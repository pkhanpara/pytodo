// src/List.js
import React from 'react';

export const List = ({ lists }) => {
  return (
    <div className="list-container">
      <h2>Todo Lists</h2>
      <ul>
        {lists.map((list, index) => (
          <li key={index}>
            <h3>{list.title}</h3>
            <ul>
              {list.items.map((item, i) => (
                <li key={i}>{item.content}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};
