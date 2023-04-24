for filename in os.listdir("tester"):
    if filename.endswith(".txt"):
        print(filename)
        main("tester/" + filename)
