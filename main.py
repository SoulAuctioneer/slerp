from main_loop import MainLoop

if __name__ == "__main__":

    # Initialize the looper
    main_loop = MainLoop()

    # Fire up the first page of the narrative
    main_loop.page_start()

    # Start the main loop running
    main_loop.run()

    # Quit, so shut down the main loop
    main_loop.shut_down()
