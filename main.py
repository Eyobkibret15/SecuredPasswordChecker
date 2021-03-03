import requests
import hashlib


def passwords_security_check():
    with open("PasswordsList.txt") as pas_list:
        passwords_list = pas_list.readlines()
        for current_password in passwords_list:
            current_password = current_password.split('\n')
            count_found = pwned_api_check(current_password[0])
            if count_found:
                print(f'{current_password[0]} is found {count_found} times you should change your password')
            else:
                print(f'{current_password[0]} is found {count_found} times carry on')
            print('checked')


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_hash1, tail_hash1 = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_hash1)
    response.text
    return password_leaks_count(response, tail_hash1)


def request_api_data(first5_hash1):
    url = 'https://api.pwnedpasswords.com/range/' + first5_hash1
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f' error code {response.status_code} found ')
    else:
        return response


def password_leaks_count(hashes, hash_to_check):
    hashses = (line.split(':') for line in hashes.text.splitlines())
    for tail, count in hashses:
        if tail == hash_to_check:
            return count
    return 0


passwords_security_check()
