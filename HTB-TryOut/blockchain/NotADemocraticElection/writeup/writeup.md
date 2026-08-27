# NotADemocraticElection

## 1. Tổng quan

- **Loại:** Blockchain (Solidity, EVM)
- **Độ khó:** Easy
- **Tác giả:** makelaris
- **Mô tả:** Trong thế giới hậu tận thế, hai phe ALF (Automata Liberation Front) và CIM (Cyborgs Independence Movement) tranh giành quyền lực. "Quyền lực được quyết định bởi tài sản" — phe nào gom đủ phiếu (vote) sẽ thắng cử.
- **Mục tiêu:** Làm cho `winner` của contract `NotADemocraticElection` trở thành `CIM` (`Setup.isSolved()` trả về `true`), rồi lấy flag từ handler.

## 2. Thông tin instance

- **Handler (menu):** `154.57.164.75:31342` — các lựa chọn:
  - `1` — Connection information (RPC, contract, private key)
  - `2` — Restart Instance
  - `3` — Get flag
- **RPC endpoint:** `http://154.57.164.75:30261` (chainId `0x7a69` = 31337, Anvil)
- **Private key:** `0x848604719485baba39fb8fa119efe30113e5eb27fb00cf1938279a35ec01f32f`
- **Address:** `0x75B6B6dD53060Ca97D102a4E31c607bCFB38b967` (balance 1 ETH)
- **Target contract:** `0xFdC6a6d53505c3EE15d5a655E2C157eC3B7225D1`
- **Setup contract:** `0x2e33a9708B90c971B331d342876dE54511A63Aa8`

## 3. Phân tích contract

Contract `NotADemocraticElection` (Solidity 0.8.25):

```solidity
uint256 constant TARGET_VOTES = 1000e18;          // cần 1000 ETH phiếu để thắng

mapping(bytes3 _id => Party) public parties;       // tổng phiếu của từng đảng
mapping(bytes _sig => Voter) public voters;        // trọng lượng phiếu theo "chữ ký"
mapping(string _name => mapping(string _surname => address)) public uniqueVoters;

function getVoterSig(string memory _name, string memory _surname) public pure returns (bytes memory) {
    return abi.encodePacked(_name, _surname);      // <-- BUG: nối chuỗi không có delimiter
}

function depositVoteCollateral(string memory _name, string memory _surname) external payable {
    require(uniqueVoters[_name][_surname] == address(0), "Already deposited");
    bytes memory voterSig = getVoterSig(_name, _surname);
    voters[voterSig].weight += msg.value;          // trọng lượng cộng dồn vào cùng sig
    uniqueVoters[_name][_surname] = msg.sender;
}

function vote(bytes3 _party, string memory _name, string memory _surname) public {
    require(uniqueVoters[_name][_surname] == msg.sender, "You cannot vote on behalf of others.");
    bytes memory voterSig = getVoterSig(_name, _surname);
    uint256 voterWeight = voters[voterSig].weight == 0 ? 1 : voters[voterSig].weight;
    parties[_party].totalvotes += 1 * voterWeight; // <-- có thể gọi vote() nhiều lần
    checkWinner(_party);
}
```

**Setup:** deploy contract với 2 đảng ALF/CIM, rồi `depositVoteCollateral{value: 100 ether}("Satoshi", "Nakamoto")`.

### Lỗ hổng

1. **`abi.encodePacked` mơ hồ (hash collision):** `abi.encodePacked("Satoshi", "Nakamoto")` và `abi.encodePacked("SatoshiNakamoto", "")` đều cho ra đúng chuỗi byte `"SatoshiNakamoto"` — tức cùng một key trong mapping `voters`. Nhưng `uniqueVoters` được kiểm tra theo **chuỗi chính xác**, nên ta có thể deposit với cặp `("SatoshiNakamoto", "")` mặc dù `("Satoshi", "Nakamoto")` đã được Setup dùng.

2. **Chia sẻ trọng lượng phiếu:** vì cùng key `"SatoshiNakamoto"`, deposit của ta cộng vào chính slot `voters["SatoshiNakamoto"].weight` — vốn đang chứa **100 ETH** của Setup. Khi vote với cặp `("SatoshiNakamoto", "")`, `uniqueVoters["SatoshiNakamoto"][""] == msg.sender` (chính ta) → hợp lệ, và trọng lượng lấy ra là **100 ETH**.

3. **Vote không giới hạn:** `vote()` không đánh dấu cử tri đã bỏ phiếu, nên cùng một cử tri có thể gọi `vote()` nhiều lần. Mỗi lần gọi cộng thêm `voterWeight` (100 ETH) vào tổng phiếu của đảng.

## 4. Khai thác

Các bước thực hiện:

1. **Deposit với cặp trùng key:** gọi `depositVoteCollateral("SatoshiNakamoto", "")` với `value = 1 wei`. Kiểm tra `uniqueVoters["SatoshiNakamoto"][""] == 0` thỏa mãn; `voters["SatoshiNakamoto"].weight` trở thành `100e18 + 1`.

2. **Bỏ phiếu 10 lần cho CIM:** gọi `vote(CIM, "SatoshiNakamoto", "")` 10 lần. Mỗi lần CIM nhận `100e18 + 1` phiếu → tổng `10 * (100e18 + 1) = 1000e18 + 10 ≥ TARGET_VOTES (1000e18)`.

3. **`checkWinner` chạy trong `vote()`** → `winner = CIM` → `Setup.isSolved() == true`.

### Kết quả on-chain

- Deposit: `0xf28e98cfcfd9eafb64c47636dc583848fae065e28bc7a7f3f8c949f8a2fbfb9d`
- 10 tx vote CIM: `0xea522980...`, `0xb360b35f...`, `0x36c55129...`, `0x473961a1...`, `0x8c340f74...`, `0x5d6df709...`, `0xd256dad5...`, `0x22f134dd...`, `0x76976b7e...`, `0xdfe36eab...` (danh sách đầy đủ trong `solve/evidence/txs.json`)
- `winner()` = `CIM`
- `getVotesCount(CIM)` = `1000000000000000000010` (1000e18 + 10)
- `Setup.isSolved()` = `true`

## 5. Lấy flag

Sau khi solve, gửi lựa chọn `3` trên handler `154.57.164.75:31342`:

```
HTB{h4sh_c0ll1s10n_t0_br1ng_b4ck_d3m0cr4cy}
```

## 6. Bài học

- **Không dùng `abi.encodePacked` với nhiều chuỗi động (string/bytes)** để làm key/identifier nếu không có delimiter — gây ra sự mơ hồ (ambiguity) giữa các bộ dữ liệu khác nhau, có thể bị khai thác để "mượn" trọng lượng phiếu của người khác. Nên dùng `abi.encode(...)` (có độ dài) hoặc `keccak256(abi.encode(...))`.
- **Cần đánh dấu cử tri đã bỏ phiếu** hoặc giảm trọng lượng sau khi vote, nếu không cùng một cử tri có thể bỏ phiếu vô hạn lần.
- Các phép kiểm tra danh tính (`uniqueVoters`) phải dùng **cùng một cơ chế key** với nơi lưu trữ dữ liệu (`voters`), tránh lệch key giữa hai mapping.
