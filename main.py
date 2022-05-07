"""
Financial program calculating loan payment amounts, number of required monthly payments, overpayment, etc.

Created to practise Python programming skills.

Based on Loan Calculator project on JetBrains Academy / Hyperskill website
https://hyperskill.org/projects/90
"""

import argparse
import math

parser = argparse.ArgumentParser()

parser.add_argument("--type",
                    # choices=["diff", "annuity"],
                    help="Choose between differentiated or annuity payment")

parser.add_argument("--principal",
                    type=int,
                    help="Loan principal")

parser.add_argument("--periods",
                    type=int,
                    help="Number of monthly periods")

parser.add_argument("--payment",
                    type=int,
                    help="Monthly payment amount")

parser.add_argument("--interest",
                    type=float,
                    help="Loan interest")


def calc_diff():
    total_paid = 0
    # Dm = P / n + i * (P - (P * (m - 1)) / n)
    for current_month in range(1, number_payments + 1):
        diff_payment = math.ceil(loan_principal / number_payments + (loan_interest / 12 / 100) *
                                 (loan_principal - (loan_principal * (current_month - 1)) / number_payments))
        total_paid += diff_payment
        print(f"Month {current_month}: payment is {diff_payment}")

    overpayment_diff = total_paid - loan_principal

    print(f"\nOverpayment = {overpayment_diff}")


def calc_annuity():
    nom_rate_powed = math.pow((loan_interest_nominal + 1), number_payments)  # (1 + i) ^ n
    # A ordinary annuity = (P * i * (1 + i) ^ n) / ((1 + i) ^ n - 1)
    annuity_payment = math.ceil(loan_principal * loan_interest_nominal * nom_rate_powed / (nom_rate_powed - 1))
    print(f"Your annuity payment = {annuity_payment}!")
    overpayment(annuity_payment, loan_principal)


def calc_principal():
    nom_rate_powed = math.pow((loan_interest_nominal + 1), number_payments)  # (1 + i) ^ n
    # P = A / ((i * (1 + i) ^ n)) / ((1 + i) ^ n - 1))
    result_principal = math.floor(monthly_payment / ((loan_interest_nominal * nom_rate_powed) / (nom_rate_powed - 1)))
    print(f"Your loan principal = {result_principal}!")
    overpayment(monthly_payment, result_principal)


def calc_years():
    monthly_log_base = 1 + loan_interest_nominal
    monthly_log_x = monthly_payment / (monthly_payment - loan_interest_nominal * loan_principal)

    monthly_result = math.ceil(math.log(monthly_log_x, monthly_log_base))

    if monthly_result > 11:
        years_result = math.floor(monthly_result / 12)

        if (years_result * 12) % monthly_result == 0:
            print(f"It will take {years_result} years to repay this loan!")

        else:
            remainder_months_result = monthly_result - (years_result * 12)

            if remainder_months_result == 1:
                print(f"It will take {years_result} years and 1 month to repay this loan!")
            else:
                print(f"It will take {years_result} years and {remainder_months_result} months to repay this loan!")

    elif monthly_result > 1:
        print(f"It will take {monthly_result} months to repay this loan!")
    else:
        print("It will take 1 month to repay this loan!")

    overpayment_years = math.ceil(monthly_payment * monthly_result - loan_principal)
    print(f"Overpayment = {overpayment_years}")


def overpayment(payment, principal):
    overpayment_result = math.ceil(payment * number_payments - principal)
    print(f"Overpayment = {overpayment_result}")


args = parser.parse_args()

calc_type = args.type

loan_interest = args.interest

if args.payment is not None:
    monthly_payment = args.payment
else:
    monthly_payment = 0

if args.principal is not None:
    loan_principal = args.principal
else:
    loan_principal = 0

if args.periods is not None:
    number_payments = args.periods
else:
    number_payments = 0

if len(vars(args)) < 4 or \
        calc_type is None or \
        (calc_type != "annuity" and calc_type != "diff") or \
        (calc_type == "diff" and monthly_payment > 0) or \
        loan_interest is None or \
        (loan_principal < 0 or number_payments < 0 or monthly_payment < 0 or loan_interest < 0):
    print("Incorrect parameters")

else:
    loan_interest_nominal = loan_interest / 12 / 100

    if calc_type == "diff":
        calc_diff()
    elif loan_principal != 0 and number_payments != 0:
        calc_annuity()
    elif number_payments == 0:
        calc_years()
    else:
        calc_principal()
