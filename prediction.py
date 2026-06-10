import joblib
import numpy as np
import pandas as pd
import sklearn

MODEL_PATH='artifacts/hotel_cancellation_rf.pkl'
FEATURE_PATH='artifacts/feature_names.pkl'

model = joblib.load(MODEL_PATH)
features=joblib.load(FEATURE_PATH)


def prepare_df(lead_time, previous_cancellations, booking_changes,
       total_of_special_requests, previous_bookings_not_canceled, adr,
       days_in_waiting_list, market_segment,
       distribution_channel,
       deposit_type,
       customer_type,
       ):

  input_data={
   'lead_time':lead_time,
   'previous_cancellations':previous_cancellations ,
   'booking_changes':booking_changes,
   'total_of_special_requests':total_of_special_requests,
   'previous_bookings_not_canceled':previous_bookings_not_canceled,
   'adr':adr,
   'days_in_waiting_list':days_in_waiting_list,
   'market_segment_Direct': 1 if market_segment == 'Direct' else 0,
   'market_segment_Groups': 1 if market_segment == 'Groups' else 0,
   'market_segment_Corporate': 1 if market_segment == 'Corporate' else 0,
   'market_segment_Offline TA/TO': 1 if market_segment == 'Offline TA/TO' else 0,
   'market_segment_Online TA': 1 if market_segment == 'Online TA' else 0,
   'market_segment_Undefined': 1 if market_segment == 'Undefined' else 0,
   'market_segment_Complementary': 1 if market_segment == 'Complementary' else 0,
   'distribution_channel_Direct': 1 if distribution_channel == 'Direct' else 0,
   'distribution_channel_channel_GDS':1 if distribution_channel == 'GDS' else 0,
   'distribution_channel_TA/TO': 1 if distribution_channel == 'TA/TO' else 0,
   'distribution_channel_Undefined': 1 if distribution_channel == 'Undefined' else 0,
   'deposit_type_Non Refund': 1 if deposit_type == 'Non Refund' else 0,
   'deposit_type_Refundable': 1 if deposit_type == 'Refundable' else 0,
   'customer_type_Group': 1 if customer_type == 'Group' else 0,
   'customer_type_Transient': 1 if customer_type == 'Transient' else 0,
   'customer_type_Transient-Party': 1 if customer_type == 'Transient-Party' else 0,

  }
  df=pd.DataFrame([input_data])

  df = df.reindex(columns=features, fill_value=0)

  return df

def predict_cancellation(df):
    probability = model.predict_proba(df)[0][1]

    prediction = 1 if probability >= 0.45 else 0

    return prediction, probability
