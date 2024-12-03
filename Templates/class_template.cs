using System;

public class {{ class_name }}
{
{% for field, field_type in fields.items() %}
	public {{ field_type }} {{ field }} { get; set; }
{% endfor %}
}