# Install and imports
import lkml

class LookerCodyGuardFunc:

  # Parameters
  abbrevs = ['GMV', 'NMV', 'BU', 'ST', 'FT', 'MP', 'PM', 'PM2', 'PM2c', 'B2B', 'B2C', 'GP', 'OSF', 'PLM', 'MNC', 'TY', 'TL', 'USD', 'EUR', 'GBP', '3D', 'SKU', 'TEX', 'NPS', 'L7D', 'L10D', 'L1W', 'L2W', 'L14D','L1M', 'L3M', 'L6M','L1Y', 'YTD', 'SC', 'MSRP', 'TCMB', 'GittiGidiyor', 'HepsiBurada', 'n11', 'ArGe', 'SC', 'CR', 'PM2%', 'PDA', 'LTM', 'L3D', 'QC', 'AB', 'Q&A', 'ABS', 'BPM', 'SPM', 'WoW', 'CTR', 'LMS', 'FCR', 'IVR', 'MD', 'PDF', 'TMS', 'SMV', 'TGO', 'TYGO', 'HR', 'KPI', 'GWS', 'PC', 'TBL', 'IBM', 'CA', 'RPA', 'POS', 'PIM', 'API', 'DYS', 'TET', 'SSF', 'AC', 'OB', 'PO', 'DYS', 'AGT', 'ETGB', 'CB', 'ABS', 'AIS', 'IPAS', 'OPAS', 'SIPAS', 'SPAS', 'E-Fatura', 'E-Arşiv', 'KVKK', 'GDPR']
  connectors = ['or', 'and', 'to', 'of', 'a', 'exc', 'on', 'in', 'at', 'by', 'the', 've', 'ile', 'veya', 'with', 'within', 'per', 'without', 'for', 'inc']
  # Functions

  # General

  def make_titlecase(self, text):
    words = text.split()
    words_v1 = []
    words_v2 = []
    for w in words:
      checked = 0
      for j in LookerCodyGuardFunc.abbrevs:
        if w.lower() == j.lower():
          words_v1.append(j)
          words_v2.append(j)
          checked = 1
          break
      if checked == 0:
        for i in LookerCodyGuardFunc.connectors:
          if w.lower() == i.lower():
            if len(words_v1) >0 :
              words_v1.append(i)
            else:
              words_v1.append(i.capitalize())
            words_v2.append(i.capitalize())
            checked = 1
            break
      if checked == 0:
        words_v1.append(w.capitalize())
        words_v2.append(w.capitalize())
    output1 = ' '.join([str(elem) for elem in words_v1])
    output2 = ' '.join([str(elem) for elem in words_v2])
    final = [output1, output2]
    return(final)

  def is_titlecase(self, text):
    titled = self.make_titlecase(text)
    st = text.rstrip()
    if st == titled[0] or st == titled[1]:
      return 1
    else:
      return 0

class LookerCodyGuard:

  def view_table_name(self, view) -> str:
    val_result = ''
    if 'derived_table' not in view.keys():
      view_name      = view['name']
      if 'extends__all' not in view.keys():
        sql_table_name = view['sql_table_name']
        table_name     = sql_table_name.partition('.')[2].replace('.','_')
        if view_name.strip().lower() != table_name.strip().lower():
          val_result = 'The view name ' + view_name + ' does not match with the table name.\n'
      else:
        extend = view['extends__all'][0][0]
        if extend.lower() not in view_name.lower():
          val_result = 'The view name ' + view_name + ' does not match with the table name.\n'
    return val_result

  def view_lower_case(self, view) -> str:
    val_result = ''
    if 'extends__all' in view.keys() or 'derived_table' in view.keys():
      view_name       = view['name']
      lower_view_name = view['name'].lower()
      if view_name != lower_view_name:
        val_result = 'The view name ' + view_name +' should be in lower case.\n'
    return val_result

  def view_label_title_case(self, view) -> str:
    funcObj = LookerCodyGuardFunc()
    val_result = ''
    view_name = view['name']
    if 'hidden' not in view.keys() or ('hidden' in view.keys() and view['hidden'] != 'yes'):
      if 'label' not in view.keys():
        val_result = 'The view name ' + view_name + ' should have a label.\n'
      else:
        label_raw = view['label']
        if '(' in label_raw:
          label = label_raw.partition('(')[0]
        else:
          label = label_raw
        if funcObj.is_titlecase(label) == 0:
          val_result = 'The label of the view ' + view_name + ' should be in title case.\n'
    return val_result

  def view_from_pbl(self, view) -> str:
    val_result = ''
    if 'extends__all' not in view.keys() and 'derived_table' not in view.keys():
      view_name      = view['name']
      sql_table_name = view['sql_table_name']
      table_schema   = (sql_table_name.partition('.')[2]).partition('.')[0]
      if 'dim' in table_schema or 'fact' in table_schema:
        val_result = 'The table used in ' + view_name + ' should be a pbl table.\n'
    return val_result


  def view_alphabetical(self, text) -> str:
    val_result = ''
    texts = [[]]
    i = 0
    char = ' '
    for line in text.splitlines():
      if len(line) != 0:
        for j in line:
          if j != ' ':
            char = j
      if char != '#':
          texts[i].append(line)
      else:
        i += 1
        texts.append([])
    parts = []
    for i in range(len(texts)):
      parts.append([])
      temp = ''
      for j in range(len(texts[i])):
        temp = temp + '\n' + texts[i][j] 
      parts[i] = temp + '}'
    for i in range(len(parts)):
      parsed_part = lkml.load(parts[i])
      if 'views' in parsed_part.keys():
        if 'name' in parsed_part['views'][0].keys():
          view_name = parsed_part['views'][0]['name']  
    for i in range(len(parts)):
      parsed_part = lkml.load(parts[i]) 
      dimensions = []
      if 'dimensions' in parsed_part.keys():
        dimensions   = parsed_part['dimensions'] 
      elif 'views' in parsed_part.keys():
        if 'dimensions' in parsed_part['views'][0].keys():
          dimensions   = parsed_part['views'][0]['dimensions']
      initials     = []
      for i in range(len(dimensions)):
        if not dimensions[i]['name'].startswith('pk_'):
          initials.append(dimensions[i]['name'][0])
      sorted_initials = sorted(initials)
      if initials != sorted_initials:
        val_result += 'The dimension fields in view ' + view_name + ' should be in alphabetical order.\n'
      dimension_groups = [] ##
      if 'dimension_groups' in parsed_part.keys(): 
        dimension_groups   = parsed_part['dimension_groups']
      elif 'views' in parsed_part.keys():
        if 'dimension_groups' in parsed_part['views'][0].keys():
          dimension_groups   = parsed_part['views'][0]['dimension_groups']
      initials     = []
      for i in range(len(dimension_groups)):
        if not dimension_groups[i]['name'].startswith('pk_'):
          initials.append(dimension_groups[i]['name'][0])
      sorted_initials = sorted(initials)
      if initials != sorted_initials:
        val_result += 'The dimension group fields in view ' + view_name + ' should be in alphabetical order.\n'
      measures = []    
      if 'measures' in parsed_part.keys():
        measures     = parsed_part['measures']
      elif 'views' in parsed_part.keys():
        if 'measures' in parsed_part['views'][0].keys():
          measures   = parsed_part['views'][0]['measures']
      initials     = []
      for i in range(len(measures)):
        if not measures[i]['name'].startswith('pk_'):
          initials.append(measures[i]['name'][0])
      sorted_initials = sorted(initials)
      if initials != sorted_initials:
        val_result += 'The measure fields in view ' + view_name + ' should be in alphabetical order.\n'
    return val_result

  def view_pk(self, view) -> str:
    val_result = ''
    view_name      = view['name']
    if 'derived_table' in view.keys():
      if 'sql' not in view['derived_table'].keys():
        if 'dimensions' in view.keys():
          dimensions = view['dimensions']
          if not dimensions[0]['name'].startswith('pk_'):
            val_result += 'The primary key of view ' + view_name + ' should start with pk_.\n'
          if 'primary_key' not in dimensions[0].keys(): 
            val_result += 'Derived table ' + view_name + ' should include a primary key defined as the first dimension of the view.\n'
          if 'primary_key' in dimensions[0].keys(): 
            if dimensions[0]['primary_key'] != 'yes':
              val_result += 'The primary_key parameter of the primary key of view ' + view_name + ' should be yes.\n'
          if 'hidden' not in dimensions[0].keys(): 
            val_result += 'Derived table ' + view_name + ' should include a hidden primary key field defined as the first dimension of the view.\n'
          if 'hidden' in dimensions[0].keys(): 
            if dimensions[0]['hidden'] != 'yes':
              val_result += 'The primary key of view ' + view_name + ' should be hidden.\n'
    return val_result

  # View - Fields

  def field_lower_case(self, view) -> str:
    val_result = ''
    view_name      = view['name']
    if 'dimensions' in view.keys():
      dimensions   = view['dimensions']
      for i in range(len(dimensions)):
        dim_name = dimensions[i]['name']
        lower_dim_name = dimensions[i]['name'].lower()
        if dim_name != lower_dim_name:
          val_result += 'The dimension field ' + dim_name + ' in view ' + view_name + ' should be in lower case.\n'
    if 'dimension_groups' in view.keys():
      dimension_groups   = view['dimension_groups']
      for i in range(len(dimension_groups)):
        dim_name = dimension_groups[i]['name']
        lower_dim_name = dimension_groups[i]['name'].lower()
        if dim_name != lower_dim_name:
          val_result += 'The dimension group field ' + dim_name + ' in view ' + view_name + ' should be in lower case.\n'
    if 'measures' in view.keys():
      measures   = view['measures']
      for i in range(len(measures)):
        measure_name     = measures[i]['name']
        lower_measure_name = measures[i]['name'].lower()
        if measure_name != lower_measure_name:
          val_result += 'The measure field ' + measure_name + ' in view ' + view_name + ' should be in lower case.\n'
    return val_result

  def field_desc(self, view) -> str:
    val_result = ''
    view_name = view['name']
    visible_fields = []
    if 'sets' in view.keys():
      for m in range(len(view['sets'])):
        if 'fields' in view['sets'][m].keys():
          for k in range(len(view['sets'][m]['fields'])):
            visible_fields.append(view['sets'][m]['fields'][k])
    if 'dimensions' in view.keys():
      dimensions = view['dimensions']
      for i in range(len(dimensions)):
        dim_name = dimensions[i]['name']
        is_dim_vis = 0
        for j in range(len(visible_fields)):
          if dim_name == visible_fields[j]:
            is_dim_vis = 1
            break
        if ('hidden' not in dimensions[i].keys() or ('hidden' in dimensions[i].keys() and dimensions[i]['hidden'] == 'no')) and 'sql' in dimensions[i].keys() and is_dim_vis == 1:
          if 'label' not in dimensions[i].keys():
            val_result += 'The label of field ' + dim_name + ' in ' + view_name + ' should be filled.\n'
          if 'description' not in dimensions[i].keys():
            val_result += 'The description of field ' + dim_name + ' in' + view_name + ' should be filled.\n'
          elif dimensions[i]['description'] == 'To be defined...' or '**' in dimensions[i]['description'] or dimensions[i]['description'] == '':
            val_result += 'The description of field ' + dim_name + ' in ' + view_name + ' should be filled.\n'
    if 'dimension_groups' in view.keys():
      dimension_groups = view['dimension_groups']
      for i in range(len(dimension_groups)):
        dim_name = dimension_groups[i]['name']
        is_dim_vis = 0
        for j in range(len(visible_fields)):
          if dim_name == visible_fields[j]:
            is_dim_vis = 1
            break      
        if ('hidden' not in dimension_groups[i].keys() or ('hidden' in dimension_groups[i].keys() and dimension_groups[i]['hidden'] == 'no')) and 'sql' in dimension_groups[i].keys() and is_dim_vis == 1:
          if 'label' not in dimension_groups[i].keys():
            val_result += 'The label of field ' + dim_name + ' in ' + view_name + ' should be filled.\n'
          if 'description' not in dimension_groups[i].keys():
            val_result += 'The description of field ' + dim_name + ' in ' + view_name + ' should be filled.\n'
          elif dimension_groups[i]['description'] == 'To be defined...' or '**' in dimension_groups[i]['description'] or dimension_groups[i]['description'] == '':
            val_result += 'The description of field ' + dim_name + ' in ' + view_name + ' should be filled.\n'
    if 'measures' in view.keys():
      measures     = view['measures']
      for i in range(len(measures)):
        measure_name = measures[i]['name']
        is_meas_vis = 0
        for j in range(len(visible_fields)):
          if measure_name == visible_fields[j]:
            is_meas_vis = 1
            break  
        if ('hidden' not in measures[i].keys() or ('hidden' in measures[i].keys() and measures[i]['hidden'] == 'no')) and 'sql' in measures[i].keys() and is_meas_vis == 1:
          if 'label' not in measures[i].keys():
            val_result += 'The label of field ' + measure_name + ' in ' + view_name + ' should be filled.\n'
          if 'description' not in measures[i].keys():
            val_result += 'The description of field ' + measure_name + ' in ' + view_name + ' should be filled.\n'
          elif measures[i]['description'] == 'To be defined...' or '**' in measures[i]['description'] or measures[i]['description'] == '':
            val_result += 'The description of field ' + measure_name + ' in ' + view_name + ' should be filled.\n'
    return val_result

  def field_value_format(self, view) -> str:
    val_result = ''
    view_name             = view['name']
    dim_numeric_list      = ['number']
    measure_numeric_list  = ['average', 
                            'average_distinct', 
                            'count', 
                            'count_distinct', 
                            'number', 
                            'percent_of_previous', 
                            'percent_of_total', 
                            'percentile', 
                            'percentile_distinct', 
                            'running_total', 
                            'sum', 
                            'sum_distinct',
                            'zipcode']
    if 'dimensions' in view.keys():
      dimensions   = view['dimensions']
      for i in range(len(dimensions)):
        if 'hidden' not in dimensions[i].keys() or ('hidden' in dimensions[i].keys() and dimensions[i]['hidden'] == 'no'):
          dim_name = dimensions[i]['name']
          if 'type' in dimensions[i].keys():
            dim_type = dimensions[i]['type']
            if dim_type in dim_numeric_list and ('value_format_name' not in dimensions[i].keys() and 'value_format' not in dimensions[i].keys()):
              val_result += 'The numeric field ' + dim_name + ' in ' + view_name + ' should have a value_format_name parameter.\n'
    if 'measures' in view.keys():
      measures   = view['measures']
      for i in range(len(measures)):
        if 'hidden' not in measures[i].keys() or ('hidden' in measures[i].keys() and measures[i]['hidden'] == 'no'):
          measure_name = measures[i]['name']
          if 'type' in measures[i].keys():
            measure_type = measures[i]['type']
            if measure_type in measure_numeric_list and ('value_format_name' not in measures[i].keys() and 'value_format' not in measures[i].keys() ):
              val_result += 'The numeric field ' + measure_name + ' in ' + view_name + ' should have a value_format_name parameter.\n' 
    return val_result

  def field_naming_1(self, view) -> str:
    val_result = ''
    view_name      = view['name']
    if 'dimension_groups' in view.keys():
      dimension_groups   = view['dimension_groups']
      for i in range(len(dimension_groups)):
        dim_name = dimension_groups[i]['name']
        if 'hidden' not in dimension_groups[i].keys() or ('hidden' in dimension_groups[i].keys() and dimension_groups[i]['hidden'] != 'yes'):
          if 'type' in dimension_groups[i].keys():
            dim_type = dimension_groups[i]['type']
            if dim_type == 'time' and ('_date' in dim_name or 'tarih' in dim_name):
              val_result += 'The time field ' + dim_name + ' in ' + view_name + ' should not end with "_date". It will be added automatically.\n'
    return val_result

  def field_naming_2(self, view) -> str:
    val_result = ''
    view_name      = view['name']
    if 'extends__all' in view.keys() or 'derived_table' in view.keys():
      if 'dimensions' in view.keys():
        dimensions   = view['dimensions']
        for i in range(len(dimensions)):
          if 'label' in dimensions[i].keys():
            dim_label = dimensions[i]['label'].lower()
            if 'supplier' in dim_label or 'merchant' in dim_label:
              val_result += 'In the field label ' + dim_label + ' in ' + view_name + ' seller should be used instead of merchant/supplier.\n'
      if 'dimension_groups' in view.keys():
        dimension_groups   = view['dimension_groups']
        for i in range(len(dimension_groups)):
          if 'label' in dimension_groups[i].keys():
            dim_label = dimension_groups[i]['label'].lower()
            if 'supplier' in dim_label or 'merchant' in dim_label or 'created' in dim_label or 'updated' in dim_label or 'modified' in dim_label:
              val_result += 'The field label ' + dim_label + ' in ' + view_name + ' violates one of the unision rules: "seller, create (date), update (date).\n'
      if 'measures' in view.keys():
        measures   = view['measures']
        for i in range(len(measures)):
          if 'label' in measures[i].keys():
            measure_label = measures[i]['label'].lower()
            if 'supplier' in measure_label or 'merchant' in measure_label:
              val_result += 'The field label ' + measure_label + ' in ' + view_name + ' seller should be used instead of merchant/supplier.\n'
    return val_result

  def field_naming_3(self, view) -> str:
    val_result = ''
    view_name      = view['name']
    if 'dimensions' in view.keys():
      dimensions   = view['dimensions']
      for i in range(len(dimensions)):
        dim_name = dimensions[i]['name']
        dim_part = dimensions[i]['name'].partition('_')[0]
        if 'type' in dimensions[i].keys():
          dim_type = dimensions[i]['type']
          if dim_type == 'yesno' and (dim_part != 'is' and dim_part != 'has'):
            val_result += 'The field name ' + dim_name + ' in ' + view_name + ' violates the rule: For the yesno fields, name should start with is_ or has_ \n'
    if 'measures' in view.keys():
      measures   = view['measures']
      for i in range(len(measures)):
        measure_name = measures[i]['name']
        measure_part = measures[i]['name'].partition('_')[0]
        if 'type' in measures[i].keys(): 
          measure_type = measures[i]['type']
          if measure_type == 'sum' and (measure_part != 'sum'): 
            val_result += 'The field name ' + measure_name + ' in ' + view_name + ' violates the rule: For the sum fields, name should start with sum_ \n'
          if measure_type == 'count' and (measure_part != 'count'): 
            val_result += 'The field name ' + measure_name + ' in ' + view_name + ' violates the rule: For the count fields, name should start with count_ \n'
          if measure_type == 'avg' and (measure_part != 'avg'):
            val_result += 'The field name ' + measure_name + ' in ' + view_name + ' violates the rule: For the avg fields, name should start with avg_ \n'
          if measure_type == 'yesno' and (measure_part != 'is' and measure_part != 'has'): 
            val_result += 'The field name ' + measure_name + ' in ' + view_name + ' violates the rule: For the yesno fields, name should start with is_ or has_ \n'
          if measure_type == 'percentile' and (measure_part != 'percent'): 
            val_result += 'The field name ' + measure_name + ' in ' + view_name + ' violates the rule: For the percentage fields, name should start with percent_ \n'
    return val_result
    
  def field_from_dimension(self, view) -> str:
    val_result = ''
    view_name      = view['name']
    if 'measures' in view.keys():
      measures     = view['measures']
      for i in range(len(measures)):
        measure_name = measures[i]['name']
        if 'sql' in measures[i].keys():
          measure_sql  = measures[i]['sql']
          if '${TABLE}' in measure_sql:
            val_result += 'The definition of the field ' + measure_name + ' in ' + view_name + ' should be from the dimensions defined rather than the field from the table.\n'
    if 'extends__all' in view.keys() or ('derived_table' in view.keys() and 'sql' not in view['derived_table'].keys()):
      if 'dimensions' in view.keys():
        dimensions = view['dimensions']
        for i in range(len(dimensions)):
          dim_name = dimensions[i]['name']
          if 'sql' in dimensions[i].keys():
            dim_sql  = dimensions[i]['sql']
            if '${TABLE}' in dim_sql:
              val_result += 'The definition of the field ' + dim_name + ' in ' + view_name + ' should be from the dimensions defined rather than the field from the table.\n'
      if 'dimension_groups' in view.keys():
        dimension_groups = view['dimension_groups']
        for i in range(len(dimension_groups)):
          dim_name = dimension_groups[i]['name']
          if 'sql' in dimension_groups[i].keys():
            dim_sql  = dimension_groups[i]['sql']
            if '${TABLE}' in dim_sql:
              val_result += 'The definition of the field ' + dim_name + ' in ' + view_name + ' should be from the dimensions defined rather than the field from the table.\n'
    return val_result

  def field_label_title_case(self, view) -> str:
    funcObj = LookerCodyGuardFunc()
    val_result = ''
    view_name = view['name']
    if 'dimensions' in view.keys():
      dimensions = view['dimensions']
      for i in range(len(dimensions)):
        dim_name = dimensions[i]['name']
        if 'label' in dimensions[i].keys():
          if '(' in dimensions[i]['label'] or '{' in dimensions[i]['label']:
            label_raw = dimensions[i]['label']
            label = ''
            is_open = 0
            for j in label_raw:
              if is_open == 0:
                if j == '(' or j == '{':
                  is_open = 1
                else:
                  label = label + j
              else:
                if j == ')' or j == '}':
                  is_open = 0
            label = ' '.join(label.split())
          else:
            label = dimensions[i]['label']
          if funcObj.is_titlecase(label) == 0:
              val_result += 'The label of the field ' + dim_name + ' in ' + view_name + ' should be in title case.\n'
    if 'dimension_groups' in view.keys():  
      dimension_groups = view['dimension_groups']
      for i in range(len(dimension_groups)):
        dim_name = dimension_groups[i]['name']
        if 'label' in dimension_groups[i].keys():
          if '(' in dimension_groups[i]['label'] or '{' in dimension_groups[i]['label']:
            label_raw = dimension_groups[i]['label']
            label = ''
            is_open = 0
            for j in label_raw:
              if is_open == 0:
                if j == '(' or j == '{':
                  is_open = 1
                else:
                  label = label + j
              else:
                if j == ')' or j == '}':
                  is_open = 0
            label = ' '.join(label.split())
          else:
            label = dimension_groups[i]['label']
          if funcObj.is_titlecase(label) == 0:
            val_result += 'The label of the field ' + dim_name + ' in ' + view_name + ' should be in title case.\n'
    if 'measures' in view.keys():
      measures = view['measures']
      for i in range(len(measures)):
        measure_name = measures[i]['name']
        if 'label' in measures[i].keys():
          if '(' in measures[i]['label'] or '{' in measures[i]['label']:
            label_raw = measures[i]['label']
            label = ''
            is_open = 0
            for j in label_raw:
              if is_open == 0:
                if j == '(' or j == '{':
                  is_open = 1
                else:
                  label = label + j
              else:
                if j == ')' or j == '}':
                  is_open = 0
            label = ' '.join(label.split())
          else:
            label = measures[i]['label']
          if funcObj.is_titlecase(label) == 0:
            val_result += 'The label of the field ' + measure_name + ' in ' + view_name + ' should be in title case.\n'
    return val_result

  def field_division_nullif(self, view):
    val_result = ''
    view_name = view['name']
    if 'extends__all' in view.keys():
      if 'measures' in view.keys():
        measures = view['measures']
        for i in range(len(measures)):
          measure_name = measures[i]['name']
          if 'sql' in measures[i].keys():
            measure_sql  = measures[i]['sql']
            if '/' in measure_sql:
              measure_part = measure_sql.partition('/')[2].lower()
              measure_part_strip = measure_part.strip()
              if '$' == measure_part_strip[0] and 'nullif' not in measure_part:
                val_result += 'The denominator of the division in field ' + measure_name + ' in ' + view_name + ' should include a NULLIF control.\n'
      if 'dimensions' in view.keys():
        dimensions = view['dimensions']
        for i in range(len(dimensions)):
          dim_name = dimensions[i]['name']
          if 'type' in dimensions[i].keys():
            if dimensions[i]['type'] == 'number':
              if 'sql' in dimensions[i].keys():
                dim_sql  = dimensions[i]['sql']
                if '/' in dim_sql:
                  dim_part = dim_sql.partition('/')[2].lower()
                  dim_part_strip = dim_part.strip()
                  if '$' == dim_part_strip[0] and 'nullif' not in dim_part:
                    val_result += 'The denominator of the division in field ' + dim_name + ' in ' + view_name + ' should include a NULLIF control.\n'
    return val_result

  # Explores

  def explore_view_def(self, explore_file) -> str:
    val_result = ''
    if 'views' in explore_file.keys():
      val_result = 'The explore files should not include a view definition.\n'
    return val_result

  def explore_parameters(self, explore_file) -> str:
    val_result = ''
    explores = explore_file['explores']
    for i in range(len(explores)):
      explore_name = explores[i]['name']
      if 'description' not in explores[i].keys(): 
        val_result += 'The explore ' + explore_name + ' should include the parameter: description.\n'
      elif explores[i]['description'] == 'To be defined...' or '**' in explores[i]['description']:
        val_result += 'The description of ' + explore_name + ' should be filled.\n'
      if 'label' not in explores[i].keys():
        val_result += 'The explore ' + explore_name + ' should include the parameter: label.\n'
      elif explores[i]['label'] == 'To be defined...' or '**' in explores[i]['label']:
        val_result += 'The label of ' + explore_name + ' should be filled.\n'
      if 'required_access_grants' not in explores[i].keys():
        val_result += 'The explore ' + explore_name + ' should include the parameter: required_access_grants.\n'
    return val_result

  def explore_relationship(self, explore_file) -> str:
    val_result = ''
    explores = explore_file['explores']
    for i in range(len(explores)):
      explore_name = explores[i]['name']
      if 'joins' in explores[i].keys(): 
        for j in range(len(explores[i]['joins'])):
          table_name = explores[i]['joins'][j]['name']
          if 'relationship' not in explores[i]['joins'][j].keys(): 
            val_result += 'The relationship parameter in the join with the table ' + table_name + ' in explore ' + explore_name + ' is missing.\n'
    return val_result

  def explore_join_subs(self, explore_file) -> str:
    val_result = ''
    explores = explore_file['explores']
    for i in range(len(explores)):
      explore_name = explores[i]['name']
      if 'joins' in explores[i].keys(): 
        for j in range(len(explores[i]['joins'])):
          table_name = explores[i]['joins'][j]['name']
          if 'sql_on' in explores[i]['joins'][j]:
            if '${TABLE}' in explores[i]['joins'][j]['sql_on']:
              val_result += 'The joins with the table ' + table_name + ' in explore ' + explore_name + ' should be built using the dimensions defined rather than the field from the table.\n'
    return val_result

  def explore_lower_case(self, explore_file) -> str:
    val_result = ''
    explores = explore_file['explores']
    for i in range(len(explores)):
      explore_name = explores[i]['name']
      if explore_name != explores[i]['name'].lower():
        val_result += 'The explore name ' + explore_name + ' should be in lower case.\n'
    return val_result

  def explore_label_title_case(self, explore_file) -> str:
    funcObj = LookerCodyGuardFunc()
    val_result = ''
    explores = explore_file['explores']
    for i in range(len(explores)):
      explore_name = explores[i]['name']
      if 'label' in explores[i].keys():
        label_raw = explores[i]['label']
        if '(' in label_raw:
          label = label_raw.partition('(')[0]
        else:
          label = label_raw
        if funcObj.is_titlecase(label) == 0:
            val_result += 'The label of the explore ' + explore_name + ' should be in title case.\n'
    return val_result

  # Error and warning functions

  def get_view_warnings(self, view) -> str:
    validation_result = 'Warnings: '
    validation_result += self.view_label_title_case(view)
    validation_result += self.field_value_format(view)
    validation_result += self.field_label_title_case(view)
    if validation_result != 'Warnings: ':
      return validation_result
    else:
      return ''

  def get_view_errors(self, view) -> str:
    validation_result = 'Errors: '
    validation_result += self.view_table_name(view)
    validation_result += self.view_lower_case(view)
    validation_result += self.view_from_pbl(view)
    validation_result += self.view_pk(view)
    validation_result += self.field_lower_case(view)
    validation_result += self.field_desc(view)
    validation_result += self.field_naming_1(view)
    validation_result += self.field_naming_2(view)
    validation_result += self.field_naming_3(view)
    validation_result += self.field_from_dimension(view)
    validation_result += self.field_division_nullif(view)
    if validation_result != 'Errors: ':
      return validation_result
    else:
      return ''

  def get_explore_warnings(self, explore_file) -> str:
    validation_result = 'Warnings: '
    validation_result += self.explore_label_title_case(explore_file)
    if validation_result != 'Warnings: ':
      return validation_result
    else:
      return ''

  def get_explore_errors(self, explore_file) -> str:
    validation_result = 'Errors: '
    validation_result += self.explore_view_def(explore_file)
    validation_result += self.explore_parameters(explore_file)
    validation_result += self.explore_relationship(explore_file)
    validation_result += self.explore_join_subs(explore_file)
    validation_result += self.explore_lower_case(explore_file)
    if validation_result != 'Errors: ':
      return validation_result
    else:
      return ''

  def check_view(self, file_path) -> str:
    validation_result = ''
    with open(file_path, 'r') as file:
      parsed_view = lkml.load(file)
      text_view = file.read()

    if 'views' in parsed_view.keys():
      view = parsed_view['views'][0]
      validation_result += self.get_view_errors(view)
      validation_result += self.get_view_warnings(view)
    validation_result += self.view_alphabetical(text_view)
    return validation_result

  def check_explore(self, file_path) -> str:
    validation_result = ''
    with open(file_path, 'r') as file:
      explore_file = lkml.load(file)
    validation_result += self.get_explore_errors(explore_file)
    validation_result += self.get_explore_warnings(explore_file)
    return validation_result

  def check_file(self, file_path) -> str:
    validation_result = ''
    with open(file_path, 'r') as file:
      parsed_file = lkml.load(file)
    if 'explores' in parsed_file.keys():
      validation_result += self.check_explore(file_path)
    elif 'views' in parsed_file.keys():
      validation_result += self.check_view(file_path)
    return validation_result
