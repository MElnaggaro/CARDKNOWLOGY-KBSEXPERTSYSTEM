import inspect

class Field:
    """Mock for experta.Field"""
    def __init__(self, type_=None, mandatory=False, default=None):
        self.type_ = type_
        self.mandatory = mandatory
        self.default = default

class Fact(dict):
    """Mock for experta.Fact"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def Rule(*patterns, salience=0):
    """Mock decorator for experta.Rule"""
    def decorator(func):
        func._is_rule = True
        func._patterns = patterns
        func._salience = salience
        return func
    return decorator

class KnowledgeEngine:
    """Mock for experta.KnowledgeEngine"""
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.fired_matches = set()
        # Find all rules in subclasses
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(method, "_is_rule"):
                self.rules.append(method)
        # Sort rules by salience
        self.rules.sort(key=lambda r: r._salience, reverse=True)

    def reset(self):
        self.facts = set()
        self.fired_matches = set()

    def declare(self, *facts):
        for f in facts:
            self.facts.add(f)

    def run(self):
        """Simple forward chaining implementation with conflict resolution."""
        while True:
            fired_any = False
            for rule in self.rules:
                # Find all possible matches for the rule
                match = self._get_match(rule)
                if match:
                    match_key = (rule.__name__, tuple(sorted(hash(f) for f in match)))
                    if match_key not in self.fired_matches:
                        rule()
                        self.fired_matches.add(match_key)
                        fired_any = True
                        # Restart to respect salience of all rules after state change
                        break 
            if not fired_any:
                break

    def _get_match(self, rule):
        """Finds a set of facts that satisfy all patterns in a rule."""
        matching_facts = []
        for pattern in rule._patterns:
            if not isinstance(pattern, Fact):
                continue
            
            found = None
            for fact in self.facts:
                if type(fact) != type(pattern):
                    continue
                
                # Check if all fields in pattern match the fact
                fields_match = True
                for key, val in pattern.items():
                    if fact.get(key) != val:
                        fields_match = False
                        break
                
                if fields_match:
                    found = fact
                    break
            
            if found:
                matching_facts.append(found)
            else:
                return None # One pattern failed
        return matching_facts
