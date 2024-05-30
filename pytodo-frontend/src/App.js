import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";
import Axios from "axios";

function App() {
    const [lists, setLists] = useState([])

    const fetchLists = async () => {
        const { data } = await Axios.get(
            "http://localhost:8000"
        );
        const lists = data["lists"];
        setLists(lists);
        console.log(lists);
        console.log(Array.isArray(lists));
        console.log(typeof (lists));
    }

    useEffect(() => {
        fetchLists();
    }, []);

    return (
        <div className="App">
            {
                lists.map((list, index) => (
                    <p key={index}>
                        <a className="App-link" href={"http://localhost:8000/list/" + list}> {list} </a>
                    </p>
                ))
            }
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    PyTodo !
                </a>
            </header>

        </div >

    );
}

export default App;
