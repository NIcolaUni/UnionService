from app import server as application, manager


if __name__ == '__main__':
    manager.run()


    use_debugger = False
    debugMode = application.config.get('DEBUG')

    if debugMode:
        use_debugger = True

        try:
            # Disable Flask's debugger if external debugger is requested
            use_debugger = not (application.config.get('DEBUG_WITH_APTANA'))
        except:
            pass
        manager.run(use_debugger=use_debugger, debug=debugMode,
                use_reloader=use_debugger, host='0.0.0.0', port=8000)

    else:
        manager.run(host='0.0.0.0', port=8000)