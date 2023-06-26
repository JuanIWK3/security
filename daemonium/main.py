import requests

# get a readme from https://github.com/pymarcus/daemonium


def get_readme():
    url = 'https://raw.githubusercontent.com/pymarcus/daemonium/master/README.md'
    response = requests.get(url)
    return response.text


def get_last_line(readme):
    lines = readme.split('\n')
    return lines[-4].replace('<pre class="marcus">', '').replace('</pre>', '').strip()


def decrypt_cesar(cypher, shift):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    decrypted = ''
    for char in cypher:
        if char in alphabet:
            decrypted += alphabet[(alphabet.index(char) +
                                   shift) % len(alphabet)]
        else:
            decrypted += char
    return decrypted


if __name__ == '__main__':
    readme = get_readme()
    last_line = get_last_line(readme)
    print(last_line)
    for i in range(0, 26):
        print(decrypt_cesar(last_line, i))
