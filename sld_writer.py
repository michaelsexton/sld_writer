import commods
import os
import errno
from sld import *


def main():
    try:
        os.makedirs('sld')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    #sld_template = StyledLayerDescriptor("template.sld")
    operating_statuses = commods.operating_statuses
    for key in commods.commods.keys():
        for status in operating_statuses.keys():
            token = key+"_"+status
            filename = token+".sld"
            #commod_filter = Filter()
            sld = StyledLayerDescriptor()
            nl = sld.create_namedlayer(get_name(commods.commods[key]))
            ustyle = nl.create_userstyle()
            ft_style = ustyle.create_featuretypestyle()
            labels=ft_style.create_rule(token+"_labels")
            labels.MaxScaleDenominator="8000000"
            labels.Filter=commod_filter(labels,commods.commods[key]) + status_filter(labels,operating_statuses[status])
            point_symbolizer(labels,status)
            #text_symbolizer(labels)
            
            no_labels = ft_style.create_rule(token)
            
            no_labels.Filter=commod_filter(no_labels,commods.commods[key]) + status_filter(no_labels,operating_statuses[status])
            no_labels.MinScaleDenominator="8000000"
            point_symbolizer(no_labels,status)
            sld.validate()
            with open(os.path.join('sld',filename), "w") as sld_file:
                sld_file.write(sld.as_sld())


def get_name(s):
    if isinstance(s, list):
        return ", ".join(s[:-1]) + ' and ' + s[-1]
    else:
        return s
        
def maxscale_rule(ft_style, token):
    rule = Rule(ft_style)

def commod_filter(rule,commod):
    c_filter = Filter(rule)
    if isinstance(commod, list):
        
        or_element=c_filter._node.makeelement('{%s}Or' % SLDNode._nsmap['ogc'])
        for c in commod:
            or_element.append(commod_filter(rule,c)._node[0])
        c_filter._node.append(or_element)
        return c_filter 
    else:
        c_filter = Filter(rule)
        prop = PropertyCriterion(c_filter,'PropertyIsLike')
        prop.PropertyName = "COMMODNAMES"
        prop.Literal = "*"+commod+"*"
        setattr(c_filter, 'PropertyIsLike', prop)
        return c_filter
    
def status_filter(rule,status):
    s_filter = Filter(rule)
    prop = PropertyCriterion(s_filter,'PropertyIsEqualTo')
    prop.PropertyName = "OPERATING_STATUS"
    prop.Literal = status
    setattr(s_filter, 'PropertyIsEqualTo', prop)
    return s_filter

def colour(status):
    colours = {"opr":"#ff0000","dps":"#ffff00","his":"#00dc00"}
    return colours[status]


def point_symbolizer(rule, status):
    ps = PointSymbolizer(rule)
    graphic = Graphic(ps)
    
    mark = Mark(graphic)
    mark.WellKnownName = 'circle'
    fill = Fill(mark)
    fill.create_cssparameter("fill",colour(status))
    stroke = Stroke(mark)
    stroke.create_cssparameter("stroke","#000000")
    stroke.create_cssparameter("stroke-width","1")
    graphic.Size = '10'
    
def text_symbolizer(rule):
    ts = TextSymbolizer(rule)
    ts._node.append(label(ts))
    font = Font(ts)
    font.create_cssparameter("font-family","Arial")
    font.create_cssparameter("font-size","12")
    font.create_cssparameter("font-style","normal")
    
    
def label(ts):
    label_element=ts._node.makeelement('{%s}Label' % SLDNode._nsmap['ogc'])
    label_property_element = ts._node.makeelement('{%s}PropertyName' % SLDNode._nsmap['sld'])
    ts._node.append(label_property_element)
    label_property_element = "NAME"
    label_element.append = label_property_element
    return label_element

main()