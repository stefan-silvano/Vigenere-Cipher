class Vigenere:

    def __init__(self):
        self.maximum_key_length = 100
        self.english_index = 0.0667
        self.english_frequencies = { 'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.2, 'e': 12.7, 'f': 2.2, 'g': 2.0, 'h': 6.1,
            'i': 7.0, 'j': 0.1, 'k': 0.8, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.1, 'r': 6.0,
            's': 6.3, 't': 9.0, 'u': 2.8, 'v': 1.0, 'w': 2.4, 'x': 2.0, 'y': 0.1, 'z': 0.1 }

    def processing(self, plaintext):

        plaintext = plaintext.lower()
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        for character in plaintext:
            if character not in alphabet:
                plaintext = plaintext.replace(character, '')

        return plaintext

    def encrypt(self, plaintext, key):

        ciphertext = ''
        plaintext = self.processing(plaintext)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        for i in range(len(plaintext)):
            letter = plaintext[i]
            key_letter = key[i % len(key)]
            letter_index = alphabet.index(letter)
            key_letter_index = alphabet.index(key_letter)
            new_index = (letter_index + key_letter_index) % 26
            ciphertext += alphabet[new_index]

        return ciphertext

    def decrypt(self, ciphertext, key):

        plaintext = ''
        ciphertext = ciphertext
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        for i in range(len(ciphertext)):
            letter = ciphertext[i]
            key_letter = key[i % len(key)]
            letter_index = alphabet.index(letter)
            key_letter_index = alphabet.index(key_letter)
            new_index = (letter_index - key_letter_index) % 26
            plaintext += alphabet[new_index]

        return plaintext

    def calculate_coincidence_index(self, ciphertext, key_length):

        streams_list = []
        stream = []
        for j in range(key_length):
            for i in range(j, len(ciphertext)):
                if i % key_length == j:
                    stream.append(ciphertext[i])
            streams_list.append(''.join(stream))
            stream = []

        coincidence_index_list = []
        for i in range(len(streams_list)):
            character_appearance = {char: 0 for char in set(ciphertext)}
            for char in streams_list[i]:
                character_appearance[char] += 1
            character_appearance_sum = sum(character_appearance.values())
            character_sum = sum(c * (c - 1) for c in character_appearance.values())
            coincidence_index = character_sum / (character_appearance_sum * (character_appearance_sum - 1))
            coincidence_index_list.append(coincidence_index)

        return sum(coincidence_index_list) / len(coincidence_index_list)

    def find_key_length(self, ciphertext):

        #Deoarece indexul de coincidenta este intre 0 si 1
        best_distance = 1
        #Cel mai bun l care corespunde si la distanta cea mai buna
        best_key_length = 0
        #Pornesc cu cheia de lungeme l pana la n (dat)
        for key_length in range(2, self.maximum_key_length):
            #Calculez indexul pentru l-ul curent
            coincidence_index = self.calculate_coincidence_index(ciphertext, key_length)
            #Vad cat de departe e de indexul lb engleze (0.0667)
            distance = abs(self.english_index - coincidence_index)
            #Daca indexul pt l curent < decat cel mai bun si daca index-ul curent si cel mai bun index > epsilon (0.01)
            if distance < best_distance and best_distance - distance > 0.01:
                best_distance = distance
                best_key_length = key_length

        return best_key_length

    def find_key(self, ciphertext, key_length):

        plaintext = ''

        for i in range(key_length):
            maximum_shift_sum = -1
            shift_index = -1
            frequencies = {letter: 0 for letter in self.english_frequencies}

            for char in ciphertext[i::key_length]:
                frequencies[char] += 1
            frequencies_sum = sum(frequencies.values())
            current_frequencies = [freq / frequencies_sum for freq in frequencies.values()]

            for shift in range(26):
                current_shift_sum = sum(freq * current_frequencies[j]
                                        for j, freq in enumerate(self.english_frequencies.values()))
                if current_shift_sum > maximum_shift_sum:
                    maximum_shift_sum = int(current_shift_sum)
                    shift_index = shift
                current_frequencies.append(current_frequencies.pop(0))

            plaintext += chr(shift_index + 97)

        return plaintext

if __name__ == '__main__':

    vigenere_object = Vigenere()
    plaintext = "Become a Viking raider raised to be a fearless warrior. " \
                "Lead your clan from icy desolation in Norway to a new home amid the lush farmlands of ninth-century England. " \
                "Find your settlement and conquer this hostile land by any means to earn a place in Valhalla." \
                "England in the age of the Vikings is a fractured nation of petty lords and warring kingdoms." \
                "Beneath the chaos lies a rich and untamed land waiting for a new conqueror. Will it be you?" \
                "Blaze your own path across England with advanced fights, brutal battles," \
                "lead fiery raids or use strategy and alliances with other leaders to bring victory." \
                "Every choice you make in combat and conversation is another step on the path to greatness." \
                "Lead a crew of raiders and launch lightning-fast surprise attacks against Saxon armies and fortresses." \
                "Claim the riches of your enemies' lands for your clan and expand your influence far beyond your growing settlement." \
                "Unleash the ruthless fighting style of a Viking warrior as you dual-wield axes, swords, or even shields against relentless foes." \
                "Decapitate opponents in close-quarters combat, riddle them with arrows, or assassinate them with your Hidden Blade." \
                "Your clan's new home grows with your legend. Customise your settlement by building upgradable structures." \
                "Unlock new features and quests by constructing a barracks, a blacksmith and a tattoo parlour."
    key = 'vikings'
    # key = 'vikingsenglandgods' works also with keys composed of several words
    encrypted = vigenere_object.encrypt(plaintext, key)
    key_length_found = vigenere_object.find_key_length(encrypted)
    key_found = vigenere_object.find_key(encrypted, key_length_found)

    print("Encrypted:", encrypted)
    print("Key lenght found:", key_length_found)
    print("Key found:", key_found)
    print("Decrypted:", vigenere_object.decrypt(encrypted, key_found))



