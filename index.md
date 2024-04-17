---
title: Azure AI Vision Exercises
permalink: index.html
layout: home
---

# Azure AI Vision Exercises

The following exercises are designed to support the modules on Microsoft Learn.


{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %}

{% for activity in labs  %}
  {% if activity.lab.title contains "Azure AI Custom Vision" %}  
    {% continue %}  
  {% endif %} 
  - [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})
{% endfor %}
