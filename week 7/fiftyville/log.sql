-- Keep a log of any SQL queries you execute as you solve the mystery.

-- This is the solution to CS50 (2022-2023) Problem Set 7 - Fiftyville. It is meant as a guide to help learners
-- reach the answers required. Understanding this, if you use this simply to get the answers and forgoe the understanding
-- of SQL then you're clearly missing on the learning outcomes the course wishes to convey. I highly encourage the use of
-- online resources and self-learning to understand the underpinning concepts (the why) of SQL for your own beneit.

-- The Thief:
SELECT people.name
FROM people
WHERE people.id IN (
    -- Get Licence Plates to person IDs
    SELECT people.id
    FROM people
    WHERE people.license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
        AND minute >= 15 AND minute <=25
        AND activity = "exit"
    )
)
AND people.id IN (
    -- Get phone numbers to IDs
    SELECT people.id
    FROM people
    WHERE people.phone_number IN (
        SELECT caller
        FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28
        AND duration < 60
    )
)
AND people.id IN (
    -- Get account number to people IDs
    SELECT people.id
    FROM people
    WHERE people.id IN (
        SELECT person_id
        FROM bank_accounts
        WHERE account_number IN (
            SELECT account_number
            FROM atm_transactions
            WHERE year = 2021 AND month = 7 AND day = 28
            AND atm_location = "Leggett Street"
            AND transaction_type = "withdraw"
            ORDER BY amount
        )
    )
)
AND people.id IN (
    -- Get Passport Numbers to people IDs
    SELECT people.id
    FROM people
    WHERE people.passport_number IN (
        SELECT passengers.passport_number
        FROM people
        JOIN passengers
        ON people.passport_number = passengers.passport_number
        JOIN flights
        ON passengers.flight_id = flights.id
        WHERE flights.year = 2021
        AND flights.month = 7 AND flights.day = 29
        AND flights.hour = 8  AND flights.minute = 20
        ORDER BY passengers.passport_number
    )
);


-- The Destination
SELECT DISTINCT airports.city
FROM flights
JOIN airports
ON airports.id = (
	SELECT flights.destination_airport_id
    FROM people
    JOIN passengers
    ON people.passport_number = passengers.passport_number
    JOIN flights
    ON passengers.flight_id = flights.id
    WHERE flights.year = 2021
    AND flights.month = 7 AND flights.day = 29
    AND people.name = "Your thief name here"
);


-- The Accomplace:
SELECT people.name
FROM people
WHERE people.phone_number IN (
	SELECT receiver
	FROM phone_calls
	WHERE year = 2021 AND month = 7 AND day = 28
	AND duration < 60
	AND caller = (
	SELECT people.phone_number
        FROM people
        WHERE people.name = "Place your thief name here"
    )
);
