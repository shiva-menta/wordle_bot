// Imports
import './App.css';
import firebase from './firebase';

import React, { useState, useEffect } from 'react';
import { useMediaQuery } from 'react-responsive';
import { motion } from "framer-motion"
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title,
  Tooltip } from 'chart.js';
import { Bar } from 'react-chartjs-2';

import SquareLoader from "react-spinners/SquareLoader";
import { FaGithub } from 'react-icons/fa';
import { TbWorld } from 'react-icons/tb';

import { collection, getDocs, orderBy, query, limit } from "firebase/firestore";

// ChartJS Information
ChartJS.register( CategoryScale, LinearScale, BarElement, Title, Tooltip);

// Main Functional Component
function App() {
  // Media Queries
  const isLargerThanSplit = useMediaQuery({ query: '(min-width: 900px)'});
  
  // State Hooks
  const [guessData, setGuessData] = useState([]);
  const [todaysWordGuesses, setTodaysWordGuesses] = useState([]);
  const [todaysWordTemplates, setTodaysWordTemplates] = useState([]);
  const [loading, setLoading] = useState(false)
  
  // Effect Hooks
  useEffect(() => {
    getFirebase();
  }, []);

  // Functions
  const getFirebase = async () => {
    setLoading(true);
    const allDocsQuerySnapshot = await getDocs(collection(firebase.firestore(), 
      "daily-game"));
    const q = query(collection(firebase.firestore(), "daily-game"), 
      orderBy('date', 'desc'), limit(1));
    const mostRecentGuessQuerySnapshot = await getDocs(q);

    const allDocs = [];
    const mostRecentGuessArray = [];
    const attemptsArray = [];
    
    allDocsQuerySnapshot.forEach((doc) => {
      allDocs.push(doc.data());
    });

    mostRecentGuessQuerySnapshot.forEach((doc) => {
      mostRecentGuessArray.push(doc.data());
    });

    allDocs.forEach((item) => {
      attemptsArray.push(item.attempts);
    })

    setGuessData(attemptsArray)
    setTodaysWordGuesses(mostRecentGuessArray[0].guesses);
    setTodaysWordTemplates(mostRecentGuessArray[0].guess_templates);

    setTimeout(() => {
      setLoading(false);
    }, 2000)
  }

  function createHeaderLogo(name, colorArr) {
    let upperCaseName = name.toUpperCase();
    let nameArr = [];

    for (let i = 0; i < upperCaseName.length; i++) {
      nameArr.push(<div key={i} className={upperCaseName[i] === ' ' ? 
        'letter-block space' : 'letter-block'} style={{backgroundColor: 
        colorArr[i]}}>{upperCaseName[i]}</div>);
    }

    return (<div className="header-logo">{nameArr}</div>);
  }
  

  // Render Method
  return (
    <div className="App">
      {loading ? (<SquareLoader size={75} color={'#6aaa64'} loading={loading}/>) : (
      <div className="wordle-bot-page">
        <div className="header">
          {isLargerThanSplit ? createHeaderLogo("Wordle Bot", ["#6aaa64", 
              "#787c7e", "#c9b458", "#787c7e", "#6aaa64", "#c9b458", "#787c7e", 
              "#787c7e", "#6aaa64", "#c9b458"]) : 
            <div className="mobile-header">
              {createHeaderLogo("Wordle", ["#6aaa64", "#787c7e", "#c9b458", 
                "#787c7e", "#6aaa64", "#c9b458"])}
              {createHeaderLogo("Bot", ["#787c7e", "#6aaa64", "#c9b458"])}
            </div>}
        </div>
        <div className="page-contents">
          <div className="split-container solution">
            <div className="section-title">Today's Solution</div>
            {guessSolutionArray(todaysWordGuesses, todaysWordTemplates)}
          </div>
          <div className="split-container performance">
            <div className="section-title">Performance Over Time</div>
            <div className="chart-sizing-container">
              {guessBarChart(guessData)}
            </div>
          </div>
        </div>
        <div className="footer">
          <div className="footer-text">V1 | Shiva Menta. 2022.</div>
          <div className="footer-links">
            <a href="https://cypher-accelerator.web.app/" target="_blank" 
              rel="noopener noreferrer"><TbWorld size={25} color={"#444647"}/>
            </a>
            <a href="https://github.com/shiva-menta" target="_blank" 
              rel="noopener noreferrer"><FaGithub size={25} color={"#444647"}/>
            </a>
          </div>
        </div>
      </div>)}
  </div>
  );
}


// Guess Display Functional Component
function guessSolutionArray(wgArr, tArr) {
  // Constants
  let counter = -1

  // Functions
  function increment(){
    counter++;
    return counter;
  }
  
  function returnColor(letter) {
    switch(letter) {
      case 'g':
        return "#6aaa64";
      case 'y':
        return "#c9b458";
      default:
        return "#787c7e";
    }
  }

  function getTodaysSolutionGrid() {
    let wordGuessArray = wgArr;
    let templatesArray = tArr;
    let renderArray = [];

    const wordVariants = {
      offscreen: {rotateY: "90deg"},
      onscreen: (i) => {return {rotateY: "0deg", transition: {
          delay: i * 0.35, duration: 0.75, ease: "easeInOut"
      }}}
    };

    for (let i = 0; i < 6; i++) {
      let temp = '';
      let template = '';

      increment();
      if (wordGuessArray[i]){
        temp = wordGuessArray[i].toUpperCase();
        template = templatesArray[i];
      } else {
        temp = template = '     ';
      }

      renderArray.push(<motion.div className="solution-row" key={i + "word"}>
        <motion.span className="letter-block" style={{backgroundColor: 
          returnColor(template[0])}} variants={wordVariants} custom={counter}>{temp[0]}
        </motion.span>
        <motion.span className="letter-block" style={{backgroundColor: 
          returnColor(template[1])}} variants={wordVariants} custom={counter}>{temp[1]}
        </motion.span>
        <motion.span className="letter-block" style={{backgroundColor: 
          returnColor(template[2])}} variants={wordVariants} custom={counter}>{temp[2]}
        </motion.span>
        <motion.span className="letter-block" style={{backgroundColor: 
          returnColor(template[3])}} variants={wordVariants} custom={counter}>{temp[3]}
        </motion.span>
        <motion.span className="letter-block" style={{backgroundColor: 
          returnColor(template[4])}} variants={wordVariants} custom={counter}>{temp[4]}
        </motion.span>
      </motion.div>)
    }

    return (<motion.div className="solution-container" initial="offscreen" 
      whileInView="onscreen" viewport={{ once:true}}>{renderArray}</motion.div>);
  }


  // Render Method
  return (getTodaysSolutionGrid());
}


// Guess Bar Chart Functional Component
function guessBarChart(totalGuessArray) {
  // Variables
  var max = 0;

  // Functions
  function createFrequencyArray(arr) {
    let guessFreqArray = [0, 0, 0, 0, 0, 0, 0];

    for (let i = 0; i < arr.length; i++) {
      guessFreqArray[arr[i] - 1] += 1;
    }
    max = Math.ceil((Math.max(...guessFreqArray) * 1.25) / 5) * 5;
    return guessFreqArray;
  }

  function getGuessPerformanceData() {
    let guessFreqArray = createFrequencyArray(totalGuessArray);
    let canvasFormattedArr = [];

    for (let i = 0; i < guessFreqArray.length; i++) {
      canvasFormattedArr.push({y: guessFreqArray[i], label: i+1});
    }

    return guessFreqArray;
  }

  function getGuessBarColors() {
    return ["#6AAA64", "#8AAD60", "#A9B15C", "#C9B458", "#AEA165", "#938F71", "#787C7E"];
  }

  // Chart Inputs
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
        max: 100,
        title: {
          display: true,
          text: "Frequency (days)"
        },
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

  const labels = ['1', '2', '3', '4', '5', '6', 'Missed'];
  const data = {
    labels,
    datasets: [
      {
        data: getGuessPerformanceData(),
        borderColor: getGuessBarColors(),
        backgroundColor: getGuessBarColors(),
      },
    ],
  };
  options.scales.y.max = max;

  
  // Render Method
  return (<Bar options={options} data={data} height="400px" width="350px"/>);
}

export default App;
