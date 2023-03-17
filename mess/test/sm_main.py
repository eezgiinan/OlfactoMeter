import sm_test as sm

traffic_light = sm.TrafficLightMachine()

traffic_light.cycle()
'Running cycle from green to yellow'

print(traffic_light.current_state.id)

print(traffic_light.current_state.name)

print(traffic_light.current_state)

print([s.id for s in traffic_light.states])

