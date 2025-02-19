from cache_warmer.main import health_check, main


def test_main():
    # only for debugging
    argv = [
        "-c",
        "config/config.conf",
    ]

    main(argv)
    assert True


def test_health_check():
    # only for debugging
    argv = [
        "-c",
        "config/health_check_config.conf",
    ]

    health_check(argv)
    assert True
