def run(app,port):
    import sys
    is_live = "ubuntu" in sys.argv[0]
    if is_live:
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port, ssl_keyfile="MAIN/privkey.pem", ssl_certfile="MAIN/fullchain.pem")
    else:
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port)


import threading

def talentov():
    run("talentov",5000)

def virar():
    run("virar",50087)

if __name__ == "__main__":
    thread1 = threading.Thread(target=talentov)
    thread2 = threading.Thread(target=virar)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()