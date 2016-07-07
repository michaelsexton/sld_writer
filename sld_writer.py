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
    all_statuses=commods.operating_statuses["with_commods"].copy()
    all_statuses.update(commods.operating_statuses["no_commods"])
    for status in all_statuses.keys():
        token = status
        if commods.operating_statuses["with_commods"].has_key(status):
            for commod in commods.commods.keys():
               if not commod is None:
                   token = commod+"_"+status
               
                   generate_sld(token,status,commod) 
        generate_sld(token,status) 
    
            
def generate_sld(token,status,commod=None):
    filename = token+".sld"
    status_dict = [a for a in commods.operating_statuses.values() if a.has_key(status)][0]
    sld = StyledLayerDescriptor()
    nl = sld.create_namedlayer(get_name(commods.commods[commod]))
    ustyle = nl.create_userstyle()
    ft_style = ustyle.create_featuretypestyle()
    labels=ft_style.create_rule(token+"_labels")
    if commod is None:
        labels.Filter=  status_filter(labels,status_dict[status])
    else:
        labels.Filter=  status_filter(labels,status_dict[status]) + commod_filter(labels,commods.commods[commod])
    labels.MaxScaleDenominator="8000000"
    point_symbolizer(labels,status)
    text_symbolizer(labels)
    
    no_labels = ft_style.create_rule(token)
    
    if commod is None:
        no_labels.Filter= status_filter(no_labels,status_dict[status])
    else:
        no_labels.Filter= status_filter(no_labels,status_dict[status]) +commod_filter(no_labels,commods.commods[commod])
    no_labels.MinScaleDenominator="8000000"
    point_symbolizer(no_labels,status)
    print filename
    #sld.validate()
    with open(os.path.join('sld',filename), "w") as sld_file:
        sld_file.write(sld.as_sld(pretty_print=True))


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
        prop._node.set("escape","!")
        prop._node.set("wildCard","*")
        prop._node.set("singleChar","#")
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
    colours = {"opr":"#ff0000","dps":"#ffff00","his":"#00dc00","cam":"#aaaaaa"}
    return colours[status]


def point_symbolizer(rule, status):
    ps = PointSymbolizer(rule)
    graphic = Graphic(ps)
    
    mark = Mark(graphic)
    mark.WellKnownName = 'circle'
    fill = Fill(mark)
    css_parameter = CssParameter(fill,0)
    css_parameter._node.attrib['name']="fill"
    css_parameter._node.text=colour(status)
    fill.CssParameter=css_parameter
    #fill.create_cssparameter("fill",colour(status))
    stroke = Stroke(mark)
    stroke.create_cssparameter("stroke","#000000")
    stroke.create_cssparameter("stroke-width","1")
    graphic.Size = '10'
    
def text_symbolizer(rule):
    ts = TextSymbolizer(rule)
    text_label = Label(ts)
    text_label.PropertyName="NAME"
    #ts._node.append(label(ts))
    font = Font(ts)
    font.create_cssparameter("font-family","Arial")
    font.create_cssparameter("font-size","12")
    font.create_cssparameter("font-style","normal")
    label_placement = LabelPlacement(ts)
    point_placement = PointPlacement(label_placement)
    anchor_point = AnchorPoint(point_placement)
    anchor_point.AnchorPointX="0.5"
    anchor_point.AnchorPointY="0.0"
    displacement = Displacement(point_placement)
    displacement.DisplacementX="0"
    displacement.DisplacementY="6"
    halo = Halo(ts)
    halo.Radius="2"
    halo_fill=Fill(halo)
    halo_fill.create_cssparameter("fill","#ffffff")
    text_fill=Fill(ts)
    text_fill.create_cssparameter("fill","#000000")


main()