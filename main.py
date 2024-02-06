import sentry_sdk

sentry_sdk.init(
    dsn="https://30b24fa91ed74de1b6e8fe93011d80ac@us.sentry.io/4506695594016768",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

division_by_zero = 1 / 0