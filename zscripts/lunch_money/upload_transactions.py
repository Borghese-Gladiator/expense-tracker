"""
DO NOT USE
1. Lunch Money has an existing Upload as CSV feature built on each account (though requires custom categorization for each transaction)
2. Need to add "payee" and "account_id" for below transactions to be useful (external_id is used to differentiate transactions inside an account)
"""

"""
07/04/2024
SUCCESS
{'ids': [2218716752, 2218716753, 2218716754, 2218716755, 2218716756, 2218716757, 2218716758, 2218716759, 2218716760, 2218716761, 2218716762, 2218716763, 2218716764, 2218716765, 2218716766, 2218716767, 2218716768, 2218716769, 2218716770, 2218716771, 2218716772, 2218716773, 2218716774, 2218716775, 2218716776, 2218716777, 2218716778, 2218716779, 2218716780, 2218716781, 2218716782, 2218716783, 2218716784, 2218716785, 2218716786, 2218716787, 2218716788, 2218716789, 2218716790, 2218716791, 2218716792, 2218716793, 2218716794, 2218716795, 2218716796, 2218716797, 2218716798, 2218716799, 2218716800, 2218716801, 2218716802, 2218716803, 2218716804, 2218716805, 2218716806, 2218716807, 2218716808, 2218716809, 2218716810, 2218716811, 2218716812, 2218716813, 2218716814, 2218716815, 2218716816, 2218716817, 2218716818, 2218716819, 2218716820, 2218716821, 2218716822, 2218716823, 2218716824, 2218716825, 2218716826, 2218716827, 2218716828, 2218716829, 2218716830, 2218716831, 2218716832, 2218716833, 2218716834, 2218716835, 2218716836, 2218716837, 2218716838, 2218716839, 2218716840, 2218716841, 2218716842, 2218716843, 2218716844, 2218716845, 2218716846, 2218716847, 2218716848, 2218716849, 2218716850, 2218716851, 2218716852, 2218716853, 2218716854, 2218716855, 2218716856, 2218716857, 2218716858, 2218716859, 2218716860, 2218716861, 2218716862, 2218716863, 2218716864, 2218716865, 2218716866, 2218716867, 2218716868, 2218716869, 2218716870, 2218716871, 2218716872, 2218716873, 2218716874, 2218716875, 2218716876, 2218716877, 2218716878, 2218716879, 2218716880, 2218716881, 2218716882, 2218716883, 2218716884, 2218716885, 2218716886, 2218716887, 2218716888, 2218716889, 2218716890, 2218716891, 2218716892, 2218716893, 2218716894, 2218716895, 2218716896, 2218716897, 2218716898, 2218716899, 2218716900, 2218716901, 2218716902, 2218716903, 2218716904, 2218716905, 2218716906, 2218716907, 2218716908, 2218716909, 2218716910, 2218716911, 2218716912, 2218716913, 2218716914, 2218716915, 2218716916, 2218716917, 2218716918, 2218716919, 2218716920, 2218716921, 2218716922, 2218716923, 2218716924, 2218716925, 2218716926, 2218716927, 2218716928, 2218716929, 2218716930, 2218716931, 2218716932, 2218716933, 2218716934, 2218716935, 2218716936, 2218716937, 2218716938, 2218716939, 2218716940, 2218716941, 2218716942, 2218716943, 2218716944, 2218716945, 2218716946, 2218716947, 2218716948, 2218716949, 2218716950, 2218716951, 2218716952, 2218716953, 2218716954, 2218716955, 2218716956, 2218716957, 2218716958, 2218716959, 2218716960, 2218716961, 2218716962, 2218716963, 2218716964, 2218716965, 2218716966, 2218716967, 2218716968, 2218716969, 2218716970, 2218716971, 2218716972, 2218716973, 2218716974, 2218716975, 2218716976, 2218716977, 2218716978, 2218716979, 2218716980, 2218716981, 2218716982, 2218716983, 2218716984, 2218716985, 2218716986, 2218716987, 2218716988, 2218716989, 2218716990, 2218716991, 2218716992, 2218716993, 2218716994, 2218716995, 2218716996, 2218716997, 2218716998, 2218716999, 2218717000, 2218717001, 2218717002, 2218717003, 2218717004, 2218717005, 2218717006]}
"""
import os

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
LUNCH_MONEY_ACCESS_TOKEN = os.getenv('LUNCH_MONEY_API_KEY')

# CONSTANTS
endpoint = "https://dev.lunchmoney.app/v1/transactions"
headers = {
    'Authorization': f'Bearer {LUNCH_MONEY_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# PARAMS
params = {
    "debit_as_negative": True,
    "transactions": [
        {"date":"2022-10-31", "amount": -5.99, "external_id": "fidelity"},
        {"date":"2022-11-07", "amount": 961.29, "external_id": "fidelity"},
        {"date":"2022-11-07", "amount": -46.96, "external_id": "fidelity"},
        {"date":"2022-11-07", "amount": -13.00, "external_id": "fidelity"},
        {"date":"2022-11-07", "amount": -135.00, "external_id": "fidelity"},
        {"date":"2022-11-08", "amount": 30.00, "external_id": "fidelity"},
        {"date":"2022-11-09", "amount": -11.92, "external_id": "fidelity"},
        {"date":"2022-11-09", "amount": -6.29, "external_id": "fidelity"},
        {"date":"2022-11-14", "amount": -9.99, "external_id": "fidelity"},
        {"date":"2022-11-21", "amount": -84.54, "external_id": "fidelity"},
        {"date":"2022-11-23", "amount": -3.26, "external_id": "fidelity"},
        {"date":"2022-11-25", "amount": -849.99, "external_id": "fidelity"},
        {"date":"2022-12-06", "amount": -29.85, "external_id": "fidelity"},
        {"date":"2022-12-07", "amount": -45.03, "external_id": "fidelity"},
        {"date":"2022-12-08", "amount": 30.00, "external_id": "fidelity"},
        {"date":"2022-12-12", "amount": -89.07, "external_id": "fidelity"},
        {"date":"2022-12-12", "amount": -10.54, "external_id": "fidelity"},
        {"date":"2022-12-12", "amount": -29.00, "external_id": "fidelity"},
        {"date":"2022-12-12", "amount": -135.00, "external_id": "fidelity"},
        {"date":"2022-12-13", "amount": -9.99, "external_id": "fidelity"},
        {"date":"2022-12-14", "amount": 1479.43, "external_id": "fidelity"},
        {"date":"2022-12-19", "amount": -170.68, "external_id": "fidelity"},
        {"date":"2022-12-19", "amount": -7.44, "external_id": "fidelity"},
        {"date":"2022-12-21", "amount": -34.20, "external_id": "fidelity"},
        {"date":"2022-12-22", "amount": -42.50, "external_id": "fidelity"},
        {"date":"2022-12-23", "amount": -23.00, "external_id": "fidelity"},
        {"date":"2022-12-23", "amount": -16.00, "external_id": "fidelity"},
        {"date":"2023-01-06", "amount": 178.12, "external_id": "fidelity"},
        {"date":"2023-01-09", "amount": 30.00, "external_id": "fidelity"},
        {"date":"2023-01-12", "amount": -30.00, "external_id": "fidelity"},
        {"date":"2023-01-13", "amount": -9.99, "external_id": "fidelity"},
        {"date":"2023-01-17", "amount": -15.92, "external_id": "fidelity"},
        {"date":"2023-01-17", "amount": -11.68, "external_id": "fidelity"},
        {"date":"2023-01-18", "amount": -41.22, "external_id": "fidelity"},
        {"date":"2023-02-01", "amount": -27.32, "external_id": "fidelity"},
        {"date":"2023-02-07", "amount": 41.22, "external_id": "fidelity"},
        {"date":"2023-02-08", "amount": 30.00, "external_id": "fidelity"},
        {"date":"2023-02-13", "amount": -0.32, "external_id": "fidelity"},
        {"date":"2023-02-13", "amount": -9.99, "external_id": "fidelity"},
        {"date":"2023-02-13", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2023-02-16", "amount": -2.46, "external_id": "fidelity"},
        {"date":"2023-02-23", "amount": -120.00, "external_id": "fidelity"},
        {"date":"2023-02-27", "amount": -284.39, "external_id": "fidelity"},
        {"date":"2023-02-27", "amount": -2.96, "external_id": "fidelity"},
        {"date":"2023-03-01", "amount": -47.05, "external_id": "fidelity"},
        {"date":"2023-03-08", "amount": 33.00, "external_id": "fidelity"},
        {"date":"2023-03-13", "amount": -64.98, "external_id": "fidelity"},
        {"date":"2023-03-13", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2023-03-13", "amount": -9.99, "external_id": "fidelity"},
        {"date":"2023-03-16", "amount": -7.87, "external_id": "fidelity"},
        {"date":"2023-03-20", "amount": -52.89, "external_id": "fidelity"},
        {"date":"2023-03-20", "amount": -33.41, "external_id": "fidelity"},
        {"date":"2023-03-21", "amount": -41.39, "external_id": "fidelity"},
        {"date":"2023-03-24", "amount": -188.76, "external_id": "fidelity"},
        {"date":"2023-03-24", "amount": -13.54, "external_id": "fidelity"},
        {"date":"2023-03-24", "amount": -7.85, "external_id": "fidelity"},
        {"date":"2023-03-24", "amount": -61.01, "external_id": "fidelity"},
        {"date":"2023-03-24", "amount": -14.77, "external_id": "fidelity"},
        {"date":"2023-03-24", "amount": -15.52, "external_id": "fidelity"},
        {"date":"2023-03-27", "amount": -20.75, "external_id": "fidelity"},
        {"date":"2023-03-27", "amount": -79.02, "external_id": "fidelity"},
        {"date":"2023-03-27", "amount": -42.27, "external_id": "fidelity"},
        {"date":"2023-03-29", "amount": -41.20, "external_id": "fidelity"},
        {"date":"2023-03-31", "amount": -31.69, "external_id": "fidelity"},
        {"date":"2023-04-03", "amount": -28.90, "external_id": "fidelity"},
        {"date":"2023-04-03", "amount": -15.78, "external_id": "fidelity"},
        {"date":"2023-04-03", "amount": -51.21, "external_id": "fidelity"},
        {"date":"2023-04-06", "amount": -63.01, "external_id": "fidelity"},
        {"date":"2023-04-10", "amount": 687.62, "external_id": "fidelity"},
        {"date":"2023-04-10", "amount": 38.00, "external_id": "fidelity"},
        {"date":"2023-04-10", "amount": -16.99, "external_id": "fidelity"},
        {"date":"2023-04-10", "amount": -10.61, "external_id": "fidelity"},
        {"date":"2023-04-11", "amount": -21.03, "external_id": "fidelity"},
        {"date":"2023-04-11", "amount": -16.36, "external_id": "fidelity"},
        {"date":"2023-04-11", "amount": -37.51, "external_id": "fidelity"},
        {"date":"2023-04-13", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2023-04-14", "amount": -32.96, "external_id": "fidelity"},
        {"date":"2023-04-14", "amount": -37.59, "external_id": "fidelity"},
        {"date":"2023-04-14", "amount": 9.67, "external_id": "fidelity"},
        {"date":"2023-04-17", "amount": -31.73, "external_id": "fidelity"},
        {"date":"2023-04-17", "amount": -7.96, "external_id": "fidelity"},
        {"date":"2023-04-17", "amount": -17.00, "external_id": "fidelity"},
        {"date":"2023-04-18", "amount": -155.20, "external_id": "fidelity"},
        {"date":"2023-04-18", "amount": -7.94, "external_id": "fidelity"},
        {"date":"2023-04-18", "amount": -1.50, "external_id": "fidelity"},
        {"date":"2023-04-20", "amount": -0.32, "external_id": "fidelity"},
        {"date":"2023-04-25", "amount": -47.91, "external_id": "fidelity"},
        {"date":"2023-04-26", "amount": -111.41, "external_id": "fidelity"},
        {"date":"2023-04-26", "amount": -49.02, "external_id": "fidelity"},
        {"date":"2023-05-01", "amount": -35.48, "external_id": "fidelity"},
        {"date":"2023-05-08", "amount": 30.00, "external_id": "fidelity"},
        {"date":"2023-05-15", "amount": -116.00, "external_id": "fidelity"},
        {"date":"2023-05-17", "amount": -20.31, "external_id": "fidelity"},
        {"date":"2023-05-22", "amount": -107.69, "external_id": "fidelity"},
        {"date":"2023-05-23", "amount": -46.83, "external_id": "fidelity"},
        {"date":"2023-05-30", "amount": -51.92, "external_id": "fidelity"},
        {"date":"2023-05-30", "amount": -40.00, "external_id": "fidelity"},
        {"date":"2023-06-05", "amount": -11.24, "external_id": "fidelity"},
        {"date":"2023-06-05", "amount": -2.40, "external_id": "fidelity"},
        {"date":"2023-06-05", "amount": -4.80, "external_id": "fidelity"},
        {"date":"2023-06-05", "amount": -10.50, "external_id": "fidelity"},
        {"date":"2023-06-08", "amount": 51.00, "external_id": "fidelity"},
        {"date":"2023-06-16", "amount": -26.76, "external_id": "fidelity"},
        {"date":"2023-06-20", "amount": -25.00, "external_id": "fidelity"},
        {"date":"2023-06-22", "amount": 1786.27, "external_id": "fidelity"},
        {"date":"2023-06-26", "amount": -80.98, "external_id": "fidelity"},
        {"date":"2023-06-29", "amount": -192.76, "external_id": "fidelity"},
        {"date":"2023-07-11", "amount": -29.64, "external_id": "fidelity"},
        {"date":"2023-07-17", "amount": -208.00, "external_id": "fidelity"},
        {"date":"2023-07-17", "amount": -28.00, "external_id": "fidelity"},
        {"date":"2023-07-17", "amount": -30.00, "external_id": "fidelity"},
        {"date":"2023-07-17", "amount": -30.00, "external_id": "fidelity"},
        {"date":"2023-07-17", "amount": -430.81, "external_id": "fidelity"},
        {"date":"2023-07-17", "amount": -127.05, "external_id": "fidelity"},
        {"date":"2023-07-18", "amount": -7.96, "external_id": "fidelity"},
        {"date":"2023-07-19", "amount": -24.80, "external_id": "fidelity"},
        {"date":"2023-07-19", "amount": -54.01, "external_id": "fidelity"},
        {"date":"2023-07-19", "amount": -28.23, "external_id": "fidelity"},
        {"date":"2023-07-20", "amount": -106.25, "external_id": "fidelity"},
        {"date":"2023-07-20", "amount": -46.49, "external_id": "fidelity"},
        {"date":"2023-07-24", "amount": -210.94, "external_id": "fidelity"},
        {"date":"2023-07-31", "amount": -58.85, "external_id": "fidelity"},
        {"date":"2023-08-01", "amount": -74.52, "external_id": "fidelity"},
        {"date":"2023-08-01", "amount": -32.00, "external_id": "fidelity"},
        {"date":"2023-08-02", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2023-08-07", "amount": -82.84, "external_id": "fidelity"},
        {"date":"2023-08-07", "amount": -26.97, "external_id": "fidelity"},
        {"date":"2023-08-07", "amount": -11.74, "external_id": "fidelity"},
        {"date":"2023-08-08", "amount": 1165.20, "external_id": "fidelity"},
        {"date":"2023-08-08", "amount": -15.92, "external_id": "fidelity"},
        {"date":"2023-08-09", "amount": -9.99, "external_id": "fidelity"},
        {"date":"2023-08-10", "amount": -11.33, "external_id": "fidelity"},
        {"date":"2023-08-10", "amount": -20.00, "external_id": "fidelity"},
        {"date":"2023-08-11", "amount": -8.93, "external_id": "fidelity"},
        {"date":"2023-08-14", "amount": -714.11, "external_id": "fidelity"},
        {"date":"2023-08-14", "amount": -20.93, "external_id": "fidelity"},
        {"date":"2023-08-14", "amount": -122.76, "external_id": "fidelity"},
        {"date":"2023-09-08", "amount": 1691.61, "external_id": "fidelity"},
        {"date":"2023-09-11", "amount": -40.75, "external_id": "fidelity"},
        {"date":"2023-09-14", "amount": -85.00, "external_id": "fidelity"},
        {"date":"2023-10-10", "amount": 125.75, "external_id": "fidelity"},
        {"date":"2023-10-16", "amount": -52.26, "external_id": "fidelity"},
        {"date":"2023-10-23", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2023-10-23", "amount": -20.10, "external_id": "fidelity"},
        {"date":"2023-10-26", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2023-10-30", "amount": -55.25, "external_id": "fidelity"},
        {"date":"2023-10-30", "amount": -100.22, "external_id": "fidelity"},
        {"date":"2023-10-30", "amount": -137.41, "external_id": "fidelity"},
        {"date":"2023-11-06", "amount": -68.79, "external_id": "fidelity"},
        {"date":"2023-11-08", "amount": 52.26, "external_id": "fidelity"},
        {"date":"2023-11-15", "amount": -21.29, "external_id": "fidelity"},
        {"date":"2023-11-20", "amount": -20.00, "external_id": "fidelity"},
        {"date":"2023-11-20", "amount": -12.00, "external_id": "fidelity"},
        {"date":"2023-11-30", "amount": -15.12, "external_id": "fidelity"},
        {"date":"2023-12-07", "amount": -5.50, "external_id": "fidelity"},
        {"date":"2023-12-08", "amount": 423.06, "external_id": "fidelity"},
        {"date":"2023-12-11", "amount": -40.00, "external_id": "fidelity"},
        {"date":"2023-12-11", "amount": -62.84, "external_id": "fidelity"},
        {"date":"2023-12-12", "amount": -89.39, "external_id": "fidelity"},
        {"date":"2023-12-18", "amount": -60.47, "external_id": "fidelity"},
        {"date":"2023-12-21", "amount": -203.98, "external_id": "fidelity"},
        {"date":"2023-12-26", "amount": -42.11, "external_id": "fidelity"},
        {"date":"2023-12-27", "amount": -28.67, "external_id": "fidelity"},
        {"date":"2023-12-29", "amount": -27.12, "external_id": "fidelity"},
        {"date":"2023-12-29", "amount": -16.47, "external_id": "fidelity"},
        {"date":"2024-01-08", "amount": 305.32, "external_id": "fidelity"},
        {"date":"2024-01-08", "amount": -5.50, "external_id": "fidelity"},
        {"date":"2024-01-10", "amount": -54.68, "external_id": "fidelity"},
        {"date":"2024-01-16", "amount": -68.23, "external_id": "fidelity"},
        {"date":"2024-01-16", "amount": -34.73, "external_id": "fidelity"},
        {"date":"2024-01-17", "amount": -50.00, "external_id": "fidelity"},
        {"date":"2024-01-18", "amount": -55.25, "external_id": "fidelity"},
        {"date":"2024-01-19", "amount": -53.12, "external_id": "fidelity"},
        {"date":"2024-01-23", "amount": -26.99, "external_id": "fidelity"},
        {"date":"2024-01-24", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-01-26", "amount": -8.35, "external_id": "fidelity"},
        {"date":"2024-01-26", "amount": -9.60, "external_id": "fidelity"},
        {"date":"2024-01-29", "amount": -306.95, "external_id": "fidelity"},
        {"date":"2024-01-31", "amount": -8.35, "external_id": "fidelity"},
        {"date":"2024-02-02", "amount": -40.16, "external_id": "fidelity"},
        {"date":"2024-02-02", "amount": -8.35, "external_id": "fidelity"},
        {"date":"2024-02-02", "amount": -9.60, "external_id": "fidelity"},
        {"date":"2024-02-05", "amount": -410.75, "external_id": "fidelity"},
        {"date":"2024-02-05", "amount": -5.50, "external_id": "fidelity"},
        {"date":"2024-02-07", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-02-08", "amount": 531.49, "external_id": "fidelity"},
        {"date":"2024-02-09", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-02-12", "amount": -133.96, "external_id": "fidelity"},
        {"date":"2024-02-12", "amount": -65.69, "external_id": "fidelity"},
        {"date":"2024-02-12", "amount": -27.29, "external_id": "fidelity"},
        {"date":"2024-02-14", "amount": 1196.91, "external_id": "fidelity"},
        {"date":"2024-02-16", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-02-21", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-02-26", "amount": -53.98, "external_id": "fidelity"},
        {"date":"2024-02-28", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-02-28", "amount": -37.59, "external_id": "fidelity"},
        {"date":"2024-03-01", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-03-04", "amount": -61.37, "external_id": "fidelity"},
        {"date":"2024-03-05", "amount": 14.88, "external_id": "fidelity"},
        {"date":"2024-03-07", "amount": -39.00, "external_id": "fidelity"},
        {"date":"2024-03-07", "amount": -17.78, "external_id": "fidelity"},
        {"date":"2024-03-11", "amount": -21.14, "external_id": "fidelity"},
        {"date":"2024-03-11", "amount": -15.93, "external_id": "fidelity"},
        {"date":"2024-03-11", "amount": -105.41, "external_id": "fidelity"},
        {"date":"2024-03-11", "amount": -23.86, "external_id": "fidelity"},
        {"date":"2024-03-11", "amount": -5.50, "external_id": "fidelity"},
        {"date":"2024-03-13", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-03-14", "amount": -399.98, "external_id": "fidelity"},
        {"date":"2024-03-15", "amount": -9.00, "external_id": "fidelity"},
        {"date":"2024-03-22", "amount": -39.61, "external_id": "fidelity"},
        {"date":"2024-03-25", "amount": -242.25, "external_id": "fidelity"},
        {"date":"2024-03-25", "amount": -27.17, "external_id": "fidelity"},
        {"date":"2024-03-25", "amount": -19.09, "external_id": "fidelity"},
        {"date":"2024-03-25", "amount": -51.00, "external_id": "fidelity"},
        {"date":"2024-03-25", "amount": -17.47, "external_id": "fidelity"},
        {"date":"2024-03-25", "amount": -20.78, "external_id": "fidelity"},
        {"date":"2024-03-27", "amount": -116.46, "external_id": "fidelity"},
        {"date":"2024-03-27", "amount": -9.60, "external_id": "fidelity"},
        {"date":"2024-03-28", "amount": -15.00, "external_id": "fidelity"},
        {"date":"2024-03-29", "amount": -202.59, "external_id": "fidelity"},
        {"date":"2024-04-01", "amount": -178.73, "external_id": "fidelity"},
        {"date":"2024-04-02", "amount": -477.80, "external_id": "fidelity"},
        {"date":"2024-04-02", "amount": -66.77, "external_id": "fidelity"},
        {"date":"2024-04-03", "amount": -257.10, "external_id": "fidelity"},
        {"date":"2024-04-03", "amount": -9.60, "external_id": "fidelity"},
        {"date":"2024-04-04", "amount": -26.56, "external_id": "fidelity"},
        {"date":"2024-04-05", "amount": -5.50, "external_id": "fidelity"},
        {"date":"2024-04-05", "amount": -35.41, "external_id": "fidelity"},
        {"date":"2024-04-05", "amount": -136.14, "external_id": "fidelity"},
        {"date":"2024-04-05", "amount": 55.20, "external_id": "fidelity"},
        {"date":"2024-04-08", "amount": 820.66, "external_id": "fidelity"},
        {"date":"2024-04-08", "amount": -79.19, "external_id": "fidelity"},
        {"date":"2024-04-08", "amount": -64.14, "external_id": "fidelity"},
        {"date":"2024-04-08", "amount": -119.10, "external_id": "fidelity"},
        {"date":"2024-04-08", "amount": -119.76, "external_id": "fidelity"},
        {"date":"2024-04-09", "amount": -7.28, "external_id": "fidelity"},
        {"date":"2024-04-09", "amount": -43.95, "external_id": "fidelity"},
        {"date":"2024-04-10", "amount": -16.00, "external_id": "fidelity"},
        {"date":"2024-04-15", "amount": -78.93, "external_id": "fidelity"},
        {"date":"2024-04-15", "amount": -17.36, "external_id": "fidelity"},
        {"date":"2024-04-15", "amount": -66.77, "external_id": "fidelity"},
        {"date":"2024-04-16", "amount": -17.48, "external_id": "fidelity"},
        {"date":"2024-04-16", "amount": -44.95, "external_id": "fidelity"},
        {"date":"2024-04-17", "amount": -155.50, "external_id": "fidelity"},
        {"date":"2024-04-17", "amount": -43.77, "external_id": "fidelity"},
        {"date":"2024-04-19", "amount": -88.41, "external_id": "fidelity"},
        {"date":"2024-04-19", "amount": -41.23, "external_id": "fidelity"},
        {"date":"2024-04-19", "amount": -8.79, "external_id": "fidelity"},
        {"date":"2024-04-19", "amount": -9.60, "external_id": "fidelity"},
        {"date":"2024-04-22", "amount": -45.46, "external_id": "fidelity"},
        {"date":"2024-04-22", "amount": -63.75, "external_id": "fidelity"},
        {"date":"2024-04-23", "amount": -71.11, "external_id": "fidelity"},
        {"date":"2024-04-24", "amount": -10.00, "external_id": "fidelity"},
        {"date":"2024-04-24", "amount": -68.43, "external_id": "fidelity"},
        {"date":"2024-04-26", "amount": -202.01, "external_id": "fidelity"},
    ],
}
try:
    resp = requests.post(endpoint, headers=headers, json=params)
    resp.raise_for_status()
    print(resp.json())
except requests.HTTPError as e:
    # possibly check response for a message
    raise e
except requests.Timeout as e:
    # request took too long
    raise e