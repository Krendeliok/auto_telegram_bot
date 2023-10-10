import React from 'react'
import Header from './components/Header/Header';
import Content from './components/Content/Content';
import About from './components/About/About';
import Concern from './components/Concern/Concern';
import Catalog from './components/Catalog/Catalog';
import Contacts from './components/Contacts/Contacts';
import Footer from './components/Footer/Footer';

import './styles/App.css';
import './styles/Icons.css';

function App() {
  const bodySetLock = (is_lock) => {
    if (is_lock) {
      document.querySelector("body").classList.add("lock");
    }
    else {
      document.querySelector("body").classList.remove("lock");
    }
  }

  return (
    <div className="wrapper">
      <Header />
      <Content/>
      <About lockBody={ bodySetLock } />
      <Concern />
      <Catalog lockBody={ bodySetLock } />
      <Contacts />
      <Footer lockBody={bodySetLock} />
    </div>
  );
}

export default App;
