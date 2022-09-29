import './App.css';
import React, { Component } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useMediaQuery } from 'react-responsive';
import { FaGithub } from 'react-icons/fa'
import { TbWorld } from 'react-icons/tb'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
);

function App() {
  const isLargerThanSplit = useMediaQuery({ query: '(min-width: 900px)'});

  function createHeaderLogo(name, colorArr) {
    let upperCaseName = name.toUpperCase()
    let nameArr = []

    for (let i = 0; i < upperCaseName.length; i++) {
      nameArr.push(<div key={i} className={upperCaseName[i] == ' ' ? 'letter-block space' : 'letter-block'} style={{backgroundColor: colorArr[i]}}>{upperCaseName[i]}</div>)
    }

    return <div className="header-logo">{nameArr}</div>
  }
  

  return (
    <div className="wordle-bot-page">
      <div className="header">
        {isLargerThanSplit ? createHeaderLogo("Wordle Bot", ["#6aaa64", "#787c7e", "#c9b458", "#787c7e", "#6aaa64", "#c9b458", "#787c7e", "#787c7e", "#6aaa64", "#c9b458"]) : 
          <div className="mobile-header">
            {createHeaderLogo("Wordle", ["#6aaa64", "#787c7e", "#c9b458", "#787c7e", "#6aaa64", "#c9b458"])}
            {createHeaderLogo("Bot", ["#787c7e", "#6aaa64", "#c9b458"])}
          </div>}
      </div>
      <div className="page-contents">
        <div className="split-container solution">
          <div className="section-title">Today's Solution</div>
          {guessSolutionArray()}
        </div>
        <div className="split-container performance">
          <div className="section-title">Performance Over Time</div>
          <div className="chart-sizing-container">
            {guessBarChart()}
          </div>
        </div>
      </div>
      <div className="footer">
        <div className="footer-text">Shiva Menta. 2022.</div>
        <div className="footer-links">
          <a href="https://cypher-accelerator.web.app/" target="_blank" rel="noopener noreferrer"><TbWorld size={25} color={"#444647"}/></a>
          <a href="https://github.com/shiva-menta" target="_blank" rel="noopener noreferrer"><FaGithub size={25} color={"#444647"}/></a>
        </div>
      </div>
    </div>
    
  );
}

function guessSolutionArray() {
  function getTodaysSolutionGrid() {
    let wordGuessArray = ["shiva", "menta", "shiva", "menta"]

    let renderArray = []

    for (let i = 0; i < 6; i++) {
      let temp = '';
      if (wordGuessArray[i]){
        temp = wordGuessArray[i].toUpperCase()
      } else {
        temp = '     '
      }

      renderArray.push(<div className="solution-row" key={i + "word"}>
          <span className="letter-block">{temp[0]}</span>
          <span className="letter-block">{temp[1]}</span>
          <span className="letter-block">{temp[2]}</span>
          <span className="letter-block">{temp[3]}</span>
          <span className="letter-block">{temp[4]}</span>
        </div>)
    }

    return <div className="solution-container">{renderArray}</div>
  }

  return (getTodaysSolutionGrid())
}

function guessBarChart() {
  function getGuessPerformanceData() {
    let guessFreqArray = [4, 3, 2, 1, 8, 10, 2]
    let canvasFormattedArr = []

    for (let i = 0; i < guessFreqArray.length; i++) {
      canvasFormattedArr.push({y: guessFreqArray[i], label: i+1, color:"green"})
    }

    return guessFreqArray
  }

  function getGuessBarColors() {
    return ["#6AAA64", "#8AAD60", "#A9B15C", "#C9B458", "#AEA165", "#938F71", "#787C7E"]
  }

  const options = {
    elements: {
      bar: {
        width: 5,
      },
    },
    legend: {
      display: false,
    },
    responsive: false,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: false,
        text: 'Bot Guess Performance Over Time',
        font: {
          family: "'Clear Sans', 'Helvetica Neue', Arial, sans-serif",
          size: 24
        }
      },
      legend: {
        labels: {
          font: {
            family: "'Clear Sans', 'Helvetica Neue', Arial, sans-serif",
            size: 16
          }
        }
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: "Frequency (days)"
        }
      },
      x: {
        title: {
          display: true,
          text: "Num. Guesses"
        },
        barPercentage: 0.4
      },
    }
    
  };

  const labels = ['1', '2', '3', '4', '5', '6', 'Missed']

  const data = {
    labels,
    datasets: [
      {
        data: getGuessPerformanceData(),
        borderColor: getGuessBarColors(),
        backgroundColor: getGuessBarColors(),
      },
    ],
  }

  return (<Bar options={options} data={data} height="400px" width="350px"/>)
}

export default App;
