# Writeup for Yet Another Chat

Writeup Link: https://ch3f.dev/post.html?slug=l3ak26

2026-08-02 · #rev
L3akCTF 2026
Yet Another Chat
Category: Reverse Engineering
Author: aseng
Just a chit chat convo in customized chat rooms. We pulled their server and client binaries; gather information about their plan!
TL;DR
After spending hours working on unpacking the binaries with x32dbg + Scylla (run & dump) and understand the crypto, it was solved by emulating the packet. sob.
What we get
Unpacking dist.zip with the password notinfected gives three files:
client.exe server.exe challenge.pcap
So we have both sides of a custom chat protocol plus a capture of a real conversation.
First look at the capture
Open challenge.pcap in Wireshark. It is all TCP on port 13371, and there are two separate connections, which makes sense for a chat server with two clients talking to each other.
Right click any packet and hit Follow > TCP Stream.
Nothing readable at all. The traffic is encrypted.
Looking at the binaries (briefly)
Both files client.exe and server.exe are 32 bit PE binaries and both are packed, and strings gives almost nothing useful.
At this point you could dig in, unpack them, and reverse the whole crypto stack. Instead, here is the shortcut.
The realization
The client binary is already a decryptor.
Whatever the encryption is, client.exe implements it, because it has to display incoming chat messages to the user. We just need to replay the captured server traffic at the real client and let it do the work for us.
The only thing to check is that the client will connect somewhere we control. since we had unpacked the binaries, running strings on it shows:
ImpossibL3aked Chat client 127.0.0.1 connect failed to %s:%d Connected to %s:%d. Type /quit to exit. Disconnected from server
Or if you just run the client.exe without anything listening, it says “connect failed to 127.0.0.1:13371” .
So it defaults to 127.0.0.1, and the pcap already told us the port is 13371. That is everything we need.
1. Export the server side of the conversation
Back in Wireshark, Follow > TCP Stream on either connection.
Then, Use the direction dropdown at the bottom to pick the server to client direction, Set Show data as to Raw and save it as srv.bin.
2. Fake the server
Set up a listener on port 13371 that dumps our captured bytes at whatever connects:
nc -lvnp 13371 < srv.bin
netcat will send the entire file when the client connects.
3. Run the client
./client.exe ImpossibL3aked Chat client Connected to 127.0.0.1:13371. Type /quit to exit. > Welcome to ImpossibL3aked Chat > Client 1: Hey how are you guys? It's been a while since our last conversation. I have been thinking to execute our next plan in Shanghai next month. > What's up ? Oh , have you bought the illegal materials that we discussed b4? The 'Kuda Lumping' and your usual flipper? > Client 2: What's up ? Oh , have you bought the illegal materials that we discussed b4? The 'Kuda Lumping' and your usual flipper? > Client 1: Yes , it's already here. You need to bring us something as well. > What is it? The medicine? > Client 2: What is it? The medicine? > Client 1: No, not that. Did you forget about the leaks ? > Oh my bad, yea I'm sending that to Michelle later > Client 2: Oh my bad, yea I'm sending that to Michelle later > Client 1: Good , also there seems to be a password in the C2 that you created. May I know that? Once we arrive at Pudong, I'll insert the USB to the server room C6175. > Yes, the password is L3AK{1t_is_@ll_jU5t_4n0th3r_d30bf_uZzZc4t!0n_game_hopeyouenjoy:)_asengishere} > Client 2: Yes, the password is L3AK{1t_is_@ll_jU5t_4n0th3r_d30bf_uZzZc4t!0n_game_hopeyouenjoy:)_asengishere} > Client 1: Thanks, i'll see you soon. > Bybye, gluck for all participants on completing the rest of L3ak challenges! > Client 2: Bybye, gluck for all participants on completing the rest of L3ak challenges! > Client 1 left > /quit > Disconnected from server
It connects, reads the frames, decrypts them, and prints the entire conversation.
L3AK{1t_is_@ll_jU5t_4n0th3r_d30bf_uZzZc4t!0n_game_hopeyouenjoy:)_asengishere}
ch3f @ 2026
