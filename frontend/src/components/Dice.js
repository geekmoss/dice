import React from 'react';
import Dice1 from '../svg/dice1.svg';
import Dice2 from '../svg/dice2.svg';
import Dice3 from '../svg/dice3.svg';
import Dice4 from '../svg/dice4.svg';
import Dice5 from '../svg/dice5.svg';
import Dice6 from '../svg/dice6.svg';


const DICE = {
    1: <img src={Dice1} alt={"Dice - value 1"} />,
    2: <img src={Dice2} alt={"Dice - value 2"} />,
    3: <img src={Dice3} alt={"Dice - value 3"} />,
    4: <img src={Dice4} alt={"Dice - value 4"} />,
    5: <img src={Dice5} alt={"Dice - value 5"} />,
    6: <img src={Dice6} alt={"Dice - value 6"} />,
}


export default function Dice({value, onClick, style}) {
    return (
        <div onClick={onClick ? () => {onClick();} : null} style={style}>
            {DICE[value]}
        </div>
    );
}