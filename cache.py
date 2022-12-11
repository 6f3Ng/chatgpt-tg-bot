from threading import Lock

class Cache:
    def __init__(self):
        self.m = {}
        self.lock = Lock()

    def set(self, key: str, conversation_id: str, parent_id: str, lastConv: str) -> None:
        with self.lock:
            if key in self.m :
                self.m[key]["conversation_id"] = conversation_id
                self.m[key]["parent_id"].append(parent_id)
                self.m[key]["lastConv"] = lastConv
            else :
                self.m[key] = {}
                self.m[key]["parent_id"] = []
                self.m[key]["conversation_id"] = conversation_id
                self.m[key]["parent_id"].append(parent_id)
                self.m[key]["lastConv"] = lastConv

    def getLastConv(self, key: str):
        with self.lock:
            if key in self.m :
                if self.m[key]["lastConv"]:
                    self.m[key]["parent_id"].pop()
                    if len(self.m[key]["parent_id"])==0:
                        return self.m[key]["conversation_id"], None, self.m[key]["lastConv"]
                    else:
                         return self.m[key]["conversation_id"], self.m[key]["parent_id"][-1], self.m[key]["lastConv"]
                else :
                    return self.m[key]["conversation_id"], None, None
            else :
                return None, None, None

    def get(self, key: str):
        with self.lock:
            if key in self.m :
                if len(self.m[key]["parent_id"]) > 3:
                    del(self.m[key]["parent_id"][0])
                    return self.m[key]["conversation_id"], self.m[key]["parent_id"][-1]
                elif len(self.m[key]["parent_id"]) > 0 and len(self.m[key]["parent_id"]) <=3:
                    return self.m[key]["conversation_id"], self.m[key]["parent_id"][-1]
                else :
                    return self.m[key]["conversation_id"], None
            else :
                return None, None

    def reset(self, key: str):
        with self.lock:
            self.m[key] = {}
            self.m[key]["conversation_id"] = "conversation_id"
            self.m[key]["parent_id"] = []
            self.m[key]["lastConv"] = None
    
    def clear(self, key: str):
        with self.lock:
            if key in self.m :
                del self.m[key]
                

# cache = Cache()
# cache.set("a","a1","a2")
# cache.set("a","b1","b2")

# print(cache.get("a"))
# print(cache.get("a"))
