# Assignment 2: Huffman Encoding using Greedy Strategy
#
# Time Complexity  -> O(n^2)  (n = number of distinct characters;
#                     each of the n-1 merges scans the list twice)
# Space Complexity -> O(n)  (tree nodes + code table)

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


def get_frequency(text):
    freq = {}
    for ch in text:
        if ch in freq:
            freq[ch] = freq[ch] + 1
        else:
            freq[ch] = 1
    return freq


def build_tree(freq):
    nodes = []
    for ch in freq:
        nodes.append(Node(ch, freq[ch]))

    while len(nodes) > 1:
        # find node with smallest frequency
        first = 0
        for i in range(len(nodes)):
            if nodes[i].freq < nodes[first].freq:
                first = i
        smallest1 = nodes.pop(first)

        # find node with next smallest frequency
        second = 0
        for i in range(len(nodes)):
            if nodes[i].freq < nodes[second].freq:
                second = i
        smallest2 = nodes.pop(second)

        merged = Node(None, smallest1.freq + smallest2.freq)
        merged.left = smallest1
        merged.right = smallest2
        nodes.append(merged)

    return nodes[0]


def build_codes(node, code, codes):
    if node is None:
        return

    if node.char is not None:
        if code == "":
            codes[node.char] = "0"
        else:
            codes[node.char] = code
        return

    build_codes(node.left, code + "0", codes)
    build_codes(node.right, code + "1", codes)


def main():
    while True:
        print("\n1. Encode a message")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            text = input("Enter the text to encode: ")
            if text == "":
                print("Text cannot be empty")
                continue

            freq = get_frequency(text)
            root = build_tree(freq)

            codes = {}
            build_codes(root, "", codes)

            print("\nCharacter : Frequency : Code")
            for ch in codes:
                print(repr(ch), ":", freq[ch], ":", codes[ch])

            encoded = ""
            for ch in text:
                encoded = encoded + codes[ch]

            print("\nOriginal size (8 bits/char):", len(text) * 8, "bits")
            print("Encoded size               :", len(encoded), "bits")
            print("Encoded bitstream:")
            print(encoded)

        elif choice == "2":
            print("Exiting.")
            break

        else:
            print("Invalid choice")


main()
