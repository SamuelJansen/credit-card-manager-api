from python_helper import TestHelper
TestHelper.run(__file__, inspectGlobals=False)
# TestHelper.run(
#     __file__,
#     runOnly = [
#         'IntervalStaticHelperTest.prefixWithZeroIfNeeded',

#         'IntervalStaticHelperTest.getCurrentClosingDateTime_when_2023_08_15_closingDay_20',
#         'IntervalStaticHelperTest.getCurrentClosingDateTime_when_2023_08_20_closingDay_20',
#         'IntervalStaticHelperTest.getCurrentClosingDateTime_when_2023_08_24_closingDay_20',
        
#         'IntervalStaticHelperTest.getNextClosingDateTime_when_2023_08_15_closingDay_20',
#         'IntervalStaticHelperTest.getNextClosingDateTime_when_2023_08_20_closingDay_20',
#         'IntervalStaticHelperTest.getNextClosingDateTime_when_2023_08_24_closingDay_20',

#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_10_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_12_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_15_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_20_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_24_closingDay_20_dueDay_12',

#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_10_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_12_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_15_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_20_closingDay_20_dueDay_12',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_24_closingDay_20_dueDay_12',

#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_15_closingDay_20_dueDay_22',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_20_closingDay_20_dueDay_22',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_22_closingDay_20_dueDay_22',
#         'IntervalStaticHelperTest.getCurrentDueDateTime_when_2023_08_24_closingDay_20_dueDay_22',

#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_15_closingDay_20_dueDay_22',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_20_closingDay_20_dueDay_22',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_22_closingDay_20_dueDay_22',
#         'IntervalStaticHelperTest.getNextDueDateTime_when_2023_08_24_closingDay_20_dueDay_22',
        
#     ]
# )