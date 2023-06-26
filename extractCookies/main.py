import datetime
import browsercookie


def get_chrome_datetime(chromedate):
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""


def get_all_cookies():
    print("Searching for all cookies...")
    cj = browsercookie.chrome()

    with open("cookies.txt", "w", encoding="utf-8") as f:
        for cookie in cj:
            f.write(f"""
            Host: {cookie.domain}
            Cookie name (session): {cookie.name}
            Cookie value: {cookie.value}
            Expires datetime (UTC): {get_chrome_datetime(cookie.expires)}
            ===============================================================
            """)


def get_cookies_by_host(host):
    print(f"Searching for cookies by host: {host}")
    cj = browsercookie.chrome()

    domain = host.split(".")[1]

    with open(domain + ".txt", "w", encoding="utf-8") as f:
        for cookie in cj:
            if cookie.domain == host:
                f.write(f"""
                Host: {cookie.domain}
                Cookie name (session): {cookie.name}
                Cookie value: {cookie.value}
                Expires datetime (UTC): {get_chrome_datetime(cookie.expires)}
                ===============================================================
                """)
    print("Done!")


def main():
    args = input("Enter host or leave blank to search for all cookies: ")
    if args:
        get_cookies_by_host(args)
    else:
        get_all_cookies()


if __name__ == "__main__":
    main()
