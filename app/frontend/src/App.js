import React from 'react'
import Header from './components/Header/Header';
import Content from './components/Content/Content';
import About from './components/About/About';
import Concern from './components/Concern/Concern';
import Catalog from './components/Catalog/Catalog';
import Contacts from './components/Contacts/Contacts';
import Footer from './components/Footer/Footer';

import bodySetLock from './utils/lockBody'

import './styles/App.css';
import './styles/Icons.css';

function App() {
  return (
    <div className="wrapper">
      <Header />
      <Content/>
      <About/>
      <Concern />
      <Catalog lockBody={ bodySetLock } />
      <Contacts />
      <Footer lockBody={bodySetLock} />
    </div>
  );
}

export default App;
