import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from database import get_connection
def calorie_chart(user_id,use_streamlit=True):
    conn=get_connection()
    df=pd.read_sql_query("SELECT * FROM food_log WHERE user_id=?",conn,params=(user_id,))
    conn.close()
    daily=df.groupby("date")["calories"].sum()
    fig,ax=plt.subplots()
    daily.plot(kind="bar", color="orange",ax=ax)
    ax.set_title("Daily Calorie Intake")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories (kcal)")
    plt.tight_layout()
    if use_streamlit:
        st.pyplot(fig)
    else:
        plt.show()


def protein_chart(user_id,use_streamlit=True):
    conn=get_connection()
    df=pd.read_sql_query("SELECT * FROM food_log WHERE user_id=?",conn,params=(user_id,))
    conn.close()
    daily=df.groupby("date")["protein"].sum()
    fig,ax=plt.subplots()
    daily.plot(kind="bar", color="blue",ax=ax)
    ax.set_title("Daily Protein Intake")
    ax.set_xlabel("Date")
    ax.set_ylabel("Protein (g)")
    plt.tight_layout()
    if use_streamlit:
        st.pyplot(fig)
    else:
        plt.show()
    


def carbs_chart(user_id,use_streamlit=True):
    conn=get_connection()
    df=pd.read_sql_query("SELECT * FROM food_log WHERE user_id=?",conn,params=(user_id,))
    conn.close()
    daily=df.groupby("date")["carbs"].sum()
    fig,ax=plt.subplots()
    daily.plot(kind="bar", color="green",ax=ax)
    ax.set_title("Daily carbohydrate Intake")
    ax.set_xlabel("Date")
    ax.set_ylabel("Carbohydrate (g)")
    plt.tight_layout()
    if use_streamlit:
        st.pyplot(fig)
    else:
        plt.show()
    


def workout_chart(user_id,use_streamlit=True):
    conn=get_connection()
    df=pd.read_sql_query("SELECT * FROM workout_log WHERE user_id=?",conn,params=(user_id,))
    conn.close() 
    df["volume"] = df["sets"] * df["reps"] * df["weight"]
    daily = df.groupby("date")["volume"].sum()
    fig,ax=plt.subplots()
    daily.plot(kind="bar", color="green",ax=ax)
    ax.set_title("Workout Volume per Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume (sets × reps × weight)")
    plt.tight_layout()
    if use_streamlit:
        st.pyplot(fig)
    else:
        plt.show()
    



