def calculate_rois(investment_data):
    rois = []
    for row in investment_data:
        try:
            initial_value = row["financials"]["initial_value"]
            final_value = row["financials"]["final_value"]
            assert initial_value >= 0 and final_value >= 0
            roi = ((final_value - initial_value) / initial_value) * 100
            rois.append(roi)
        except (ZeroDivisionError, TypeError, KeyError) as e:
            pass
    return rois

