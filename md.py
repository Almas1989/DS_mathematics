import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Any

def create_figure(a: float, b: float, c: float, d: float, grid_range: int = 5, grid_step: int = 1
                 ) -> go.Figure:
    """
    Создаёт фигуру с двумя подграфиками (1x2):

    1) Исходное пространство и единичный квадрат.
    2) Деформированное пространство с образом единичного квадрата.

    Параметры:
        a, b, c, d (float): Элементы матрицы A = [[a, b], [c, d]].
        grid_range (int): Диапазон значений координатной сетки.
        grid_step (int): Шаг между линиями сетки.

    Возвращает:
        go.Figure: Фигура с двумя подграфиками.
    """
    # Создаём сетку координат
    xs: np.ndarray = np.arange(-grid_range, grid_range + grid_step, grid_step)
    ys: np.ndarray = np.arange(-grid_range, grid_range + grid_step, grid_step)
    matrix: np.ndarray = np.array([[a, b], [c, d]])

    # Создаём подграфики
    fig: go.Figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Исходное пространство", "Деформированное пространство"],
        horizontal_spacing=0.02
    )

    def add_vector_annotation(x: float, y: float, xref: str, yref: str,
                              color: str, label: str,
                              row: int = 1, col: int = 1,
                              text_xshift: int = 10, text_yshift: int = -10) -> None:
        """
        Добавляет на фигуру стрелку (от (0,0) до (x,y)) и текстовую подпись рядом.
        """
        # Стрелка
        fig.add_annotation(
            x=x, y=y,
            ax=0, ay=0,
            xref=xref, yref=yref,
            axref=xref, ayref=yref,
            showarrow=True,
            arrowhead=3,
            arrowcolor=color,
            arrowsize=1.0,
            arrowwidth=2,
            text="",
            row=row,
            col=col
        )
        # Подпись вектора
        fig.add_annotation(
            x=x, y=y,
            xref=xref, yref=yref,
            text=label,
            showarrow=False,
            xshift=text_xshift,
            yshift=text_yshift,
            row=row,
            col=col
        )

    # -----------------------------
    # 1) Исходное пространство
    # -----------------------------
    # Рисуем координатную сетку
    for x_val in xs:
        fig.add_trace(
            go.Scatter(
                x=[x_val, x_val],
                y=[-grid_range, grid_range],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
    for y_val in ys:
        fig.add_trace(
            go.Scatter(
                x=[-grid_range, grid_range],
                y=[y_val, y_val],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )

    # Рисуем базис: i, j
    add_vector_annotation(1, 0, "x", "y", "red", "i", row=1, col=1)
    add_vector_annotation(0, 1, "x", "y", "green", "j", row=1, col=1)

    # Рисуем единичный квадрат (параллелограмм) в исходном пространстве
    square: np.ndarray = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    fig.add_trace(
        go.Scatter(
            x=square[:, 0],
            y=square[:, 1],
            mode='lines',
            fill='toself',
            fillcolor='rgba(255,165,0,0.15)',  # оранжевый, прозрачность 15%
            line=dict(color='orange'),
            showlegend=False
        ),
        row=1, col=1
    )

    fig.update_xaxes(range=[-grid_range, grid_range], scaleanchor="y", scaleratio=1, row=1, col=1)
    fig.update_yaxes(range=[-grid_range, grid_range], row=1, col=1)

    # -----------------------------
    # 2) Деформированное пространство
    # -----------------------------
    for x_val in xs:
        line_y = np.linspace(-grid_range, grid_range, 100)
        original_points = np.array([[x_val, y_val] for y_val in line_y])
        transformed = original_points @ matrix.T
        fig.add_trace(
            go.Scatter(
                x=transformed[:, 0],
                y=transformed[:, 1],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=2
        )
    for y_val in ys:
        line_x = np.linspace(-grid_range, grid_range, 100)
        original_points = np.array([[x_val, y_val] for x_val in line_x])
        transformed = original_points @ matrix.T
        fig.add_trace(
            go.Scatter(
                x=transformed[:, 0],
                y=transformed[:, 1],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=2
        )

    # Образы базиса: i -> i' и j -> j'
    i_prime: np.ndarray = matrix @ np.array([1, 0])
    j_prime: np.ndarray = matrix @ np.array([0, 1])
    add_vector_annotation(i_prime[0], i_prime[1], "x2", "y2", "red", "i'", row=1, col=2)
    add_vector_annotation(j_prime[0], j_prime[1], "x2", "y2", "green", "j'", row=1, col=2)

    # Рисуем образ единичного квадрата в деформированном пространстве
    square_transformed: np.ndarray = square @ matrix.T
    fig.add_trace(
        go.Scatter(
            x=square_transformed[:, 0],
            y=square_transformed[:, 1],
            mode='lines',
            fill='toself',
            fillcolor='rgba(255,165,0,0.15)',
            line=dict(color='orange'),
            showlegend=False
        ),
        row=1, col=2
    )

    # Настройка осей и размеров подграфиков
    fig.update_layout(
        width=1000,
        height=500,
        margin=dict(l=0, r=0, t=50, b=50),
        xaxis=dict(
            domain=[0, 0.45],
            range=[-grid_range, grid_range],
            scaleanchor="y",
            scaleratio=1,
            constrain="domain"
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[-grid_range, grid_range],
            scaleanchor="x",
            scaleratio=1,
            constrain="domain"
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            range=[-grid_range, grid_range],
            scaleanchor="y2",
            scaleratio=1,
            constrain="domain"
        ),
        yaxis2=dict(
            domain=[0, 1],
            range=[-grid_range, grid_range],
            scaleanchor="x2",
            scaleratio=1,
            constrain="domain"
        )
    )

    return fig

def main() -> None:
    """Главная функция приложения Streamlit."""
    st.title("Интерактивная визуализация линейной деформации")

    st.subheader("Коэффициенты матрицы линейного отображения")
    col1, col2 = st.columns(2)
    a: float = col1.number_input("a:", value=1.0, step=0.1)
    b: float = col2.number_input("b:", value=0.0, step=0.1)
    col3, col4 = st.columns(2)
    c: float = col3.number_input("c:", value=0.0, step=0.1)
    d: float = col4.number_input("d:", value=1.0, step=0.1)

    # Вычисляем площадь (|det A|) и выводим в отдельном блоке
    matrix: np.ndarray = np.array([[a, b], [c, d]])
    area_scale: float = np.linalg.det(matrix)
    st.markdown(f"**det A:** {area_scale:.2f}")
    st.markdown(f"**Изменение площади (|det A|):** {abs(area_scale):.2f}")
    
    fig: go.Figure = create_figure(a, b, c, d)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
    
