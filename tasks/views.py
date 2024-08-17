from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
import plotly.express as px


# Create your views here.
def matrix(request):

    # Handle task submissions
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('matrix')

    else:
        form = TaskForm()

    tasks = Task.objects.all()

    # Prep data for plotting
    task_data = {
        'Title': [task.title for task in tasks],
        'Impact': [task.impact for task in tasks],
        'Effort': [task.effort for task in tasks],
        'Priority': [task.priority for task in tasks],
        'URL': [f"/task/{task.pk}/" for task in tasks]
    }

    # Create scatter plot
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

    # Limit axis
    fig.update_layout(
        shapes=[
            dict(
                type='line', x0=5, x1=5, y0=0, y1=10,
                line=dict(color='Black', dash='dash')
            ),
            dict(
                type='line', x0=0, x1=10, y0=5, y1=5,
                line=dict(color='Black', dash='dash')
            )
        ],
        xaxis=dict(range=[0, 10.1]),
        yaxis=dict(range=[0, 10.1]),
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


    return render(request, 'tasks/matrix.html', {'graph': graph_html, 'form': form})
