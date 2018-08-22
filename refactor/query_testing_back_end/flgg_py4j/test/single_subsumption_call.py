from py4j.java_gateway import JavaGateway

subsumer_string = 'p(X),q(X).'
subsubsumee_string = 'p(a),p(b),q(c).'

gateway = JavaGateway()

subsumer_app = gateway.entry_point
does_subsume = subsumer_app.subsumes(subsumer_string, subsubsumee_string)

print(does_subsume)