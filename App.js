import React, { Component } from 'react';
import {
  ReactiveBase,
  ReactiveList,
  DataSearch,
  SingleList,
  CategorySearch,
  SingleRange,
  ResultCard,
  DateRange,
  MultiList,
  RangeSlider
} from '@appbaseio/reactivesearch';

import './App.css';
class App extends Component {
  render() {
    return (
      <ReactiveBase
        app="practice1"
        url= "http://localhost:9200"
      >
     <DateRange
                componentId="DateSensor"
                title="search by date"
                autoSuggest={true}
                dataField="date"
                queryFormat="date"
              />
              <ReactiveList
                size={200}
                dataField="time"
                stream={true}
                pagination={false}
                showResultStats={true}
                react={{
                  "and": ["DateSensor"]
                }}
                componentId="SearchResult">
                {({
                  loading,
                  error,
                  rawData,
                  data,
                }) => 
                
                data.map(item=>
                  <ReactiveList.ResultCardsWrapper>

                    <ResultCard key={item._id}>
                      <div>
                        <img src={item.val} alt=" " width="100%" height="100%" />

                      </div>
                      <ResultCard.Title
                        dangerouslySetInnerHTML={{
                          __html: item.date
                        }}
                      />
                      <ResultCard.Description>
                        <div>
                          <div><b>time : </b> {item.date}</div></div>
                      </ResultCard.Description>
                    </ResultCard>
                  </ReactiveList.ResultCardsWrapper>
                 ) 
                 }
                 
                </ReactiveList>
      </ReactiveBase>
    );
  }
}export default App;