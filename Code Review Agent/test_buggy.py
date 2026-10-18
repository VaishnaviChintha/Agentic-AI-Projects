import time

# Hardcoded secret (Security risk)
API_KEY = "sk_live_999888777666555444"

def process_user_records(user_list, cache={}):
    # Dangerous mutable default argument bug
    results = []
    
    for i in range(len(user_list)):
        user = user_list[i]
        
        # Inefficient string concatenation in a loop (Performance issue)
        log_msg = ""
        log_msg = log_msg + "Processing user: " + str(user.get('name'))
        print(log_msg)
        
        try:
            # Potential division by zero or KeyError
            score = user['total_points'] / user['actions_count']
            
            if user['active'] == True:
                results.append({'name': user['name'], 'score': score})
                
        except:
            # Bare except clause swallowing all errors (Bad practice / Bug hiding)
            pass
            
    return results