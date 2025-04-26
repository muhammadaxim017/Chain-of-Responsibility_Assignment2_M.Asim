# 1. Request Class
class Request:
    def __init__(self, request_id, data, client_ip):
        # Request ka ID, data aur client ka IP address store karna
        self.request_id = request_id
        self.data = data
        self.client_ip = client_ip

# 2. Handler Base Class
class Handler:
    def __init__(self):
        # Next handler ka reference store karna
        self.next_handler = None

    def set_next(self, handler):
        # Chain mein agla handler set karna
        self.next_handler = handler
        return handler

    def handle(self, request):
        # Request ko agli chain mein bhejna
        if self.next_handler:
            return self.next_handler.handle(request)

# 3. Data Validation Handler
class DataValidationHandler(Handler):
    def handle(self, request):
        # Request ka data validate karna
        if not request.data or not isinstance(request.data, str):
            print(f"[Validation Failed] Request {request.request_id}: Data ghalat hai")
            return False
        print(f"[Validation Passed] Request {request.request_id}")
        return super().handle(request)

# 4. IP Filtering Handler
class IPFilterHandler(Handler):
    # Blocked IP addresses ki list
    blocked_ips = ["192.168.1.10", "10.0.0.5"]

    def handle(self, request):
        # IP check karna ke block to nahi hai
        if request.client_ip in self.blocked_ips:
            print(f"[Blocked IP] Request {request.request_id}: IP {request.client_ip} blocked hai")
            return False
        print(f"[IP Check Passed] Request {request.request_id}")
        return super().handle(request)

# 5. Caching Handler
class CachingHandler(Handler):
    # Cache mein pehle se maujood responses
    cache = {"123": "Cached response for request 123"}

    def handle(self, request):
        # Check karna ke request already cache mein hai ya nahi
        if request.request_id in self.cache:
            print(f"[Cache Hit] Request {request.request_id}: {self.cache[request.request_id]}")
            return False
        print(f"[Cache Miss] Request {request.request_id}")
        return super().handle(request)

# 6. Final Processing Handler
class FinalProcessingHandler(Handler):
    def handle(self, request):
        # Agar saare checks pass ho jayein to final processing karna
        print(f"[Final Processing] Request {request.request_id} successfully process hogaya")
        return True

# 7. Chain Setup karna
# Saare handlers ko sequence mein connect karna
data_validator = DataValidationHandler()
ip_filter = IPFilterHandler()
caching = CachingHandler()
final_processor = FinalProcessingHandler()

# Handlers ko chaining ke zariye link karna
data_validator.set_next(ip_filter).set_next(caching).set_next(final_processor)

# 8. Alag alag requests ke sath test karna
# a) Valid request ka test
print("\n--- Test 1: Valid Request ---")
request1 = Request("001", "Valid data", "192.168.1.5")
data_validator.handle(request1)

# b) Blocked IP ke sath request ka test
print("\n--- Test 2: Blocked IP Request ---")
request2 = Request("002", "Valid data", "192.168.1.10")
data_validator.handle(request2)

# c) Cached request ka test
print("\n--- Test 3: Cached Request ---")
request3 = Request("123", "Some other data", "192.168.1.5")
data_validator.handle(request3)
