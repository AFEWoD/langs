from xml.dom.minidom import parse
import sys
import FloydWarshal

def GetEdge( value ) :
    return int( value.value ) - 1

def CalculateResistance( a, b ) :
    if a == 0 :
        return b
    if b == 0 :
        return a
    return float( ( a * b ) / ( a + b ) )

def ProcessResistors( resistors, weigthts ) :
    for resistor in resistors :
        edge1 = GetEdge( resistor.attributes['net_from'] )
        edge2 = GetEdge( resistor.attributes['net_to'] )
        currentValue = weights[edge1][edge2]
        reversedCurrentValue = weights[edge2][edge1]
        value = float( resistor.attributes['resistance'].value )
        weights[edge1][edge2] = CalculateResistance( currentValue, value )
        weights[edge2][edge1] = CalculateResistance( reversedCurrentValue, value )

def ProcessCapactors( capactors, weights ) :
    ProcessResistors( capactors, weights )

def ProcessDiods( capactors, weigthts ) :
    for diode in diods :
        edge1 = GetEdge( diode.attributes['net_from'] )
        edge2 = GetEdge( diode.attributes['net_to'] )
        currentValue = weights[edge1][edge2]
        reversedCurrentValue = weights[edge2][edge1]
        value = float( diode.attributes['resistance'].value )
        reversedValue = float( diode.attributes['reverse_resistance'].value )
        weights[edge1][edge2] = CalculateResistance( currentValue, value )
        weights[edge2][edge1] = CalculateResistance( reversedCurrentValue, reversedValue )

input = parse( sys.argv[1] )
weights = []

ids = input.getElementsByTagName( 'net' )
for i in range( len( ids ) ):
    weights.append( [0] * len( ids ) )

resistors = input.getElementsByTagName( 'resistor' )
ProcessResistors( resistors, weights ) 

capactors = input.getElementsByTagName( 'capactor' )
ProcessCapactors( capactors, weights )

diods = input.getElementsByTagName( 'diode' )
ProcessDiods( diods, weights )

result = FloydWarshal.ProcessFloydWarshal( weights )

output = open( ( sys.argv[2] ), 'w' )
for a in result :
	for b in a :
		output.write( str( '{0:.7f}'.format( b ) ) + ',' )

	output.write('\n')

output.close()
