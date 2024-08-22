import React from 'react';
import '../CSS/Loading.css'
import { BeatLoader } from 'react-spinners';

function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-spinner">
        <BeatLoader color={'#123abc'} loading={true} size={15} />
      </div>
    </div>
  );
}

export default Loading;