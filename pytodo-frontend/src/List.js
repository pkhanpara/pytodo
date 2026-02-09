// src/List.js
import React from 'react';

export const List = ({ lists }) => {
  return (
    <div className="list-container">
      <h2>Todo Lists</h2>
      <ul>
        {lists.map((list, index) => (
          <li key={index}>
            {/* If list is a string (name only) */}
            {typeof list === 'string' ? (
              <h3>{list}</h3>
            ) : (
              <>
                <h3>{list.name}</h3>
                {Array.isArray(list.items) && list.items.length > 0 && (
                  <ul>
                    {list.items.map((item, i) => (
                      <li key={i}>{item.name}</li>
                    ))}
                  </ul>
                )}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};
