from django.shortcuts import render
from .models import Task
import plotly.express as px
import plotly.graph_objects as go

# Create your views here.
def matrix(request):

    tasks = Task.objects.all()

    #Prep data for plotting
    task_data = {
        'Title': [task.title for task in tasks],
        'Impact': [task.impact for task in tasks],
        'Effort': [task.effort for task in tasks],
        'Priority': [task.priority for task in tasks],
        'URL': [f"/task/{task.pk}/" for task in tasks]
    }

    #Create scatter plot
    fig = px.scatter(
        task_data,
        x="Impact",
        y="Effort",
        color="Priority",
        hover_name='Title',
        custom_data=['URL'],
        labels={
            'Impact': 'Impact (1-10)',
            'Effort': 'Effort (1-10)'
        },
        title='Impact/Effort Matrix',
        width=800,
        height=600
    )

    # Make tasks clickable
    fig.update_traces(
        marker=dict(size=12, opacity=0.8),
        hovertemplate='<b>%{hovertext}</b><extra></extra>',
        mode='markers+text',
        textposition='top center'
    )

    fig.update_layout(
        clickmode='event+select'
    )

    graph_html = fig.to_html(full_html=False)

    return render(request, 'tasks/matrix.html', {'graph': graph_html})
