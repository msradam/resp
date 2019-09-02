import React from 'react';
import { ReactTypeformEmbed } from 'react-typeform-embed'


class Survey extends React.Component {
  constructor(props) {
    super(props);
    this.openForm = this.openForm.bind(this);
  }

  openForm() {
    this.typeformEmbed.typeform.open();
  }

  render() {
    return (
      <>
        <ReactTypeformEmbed
          popup
          autoOpen={false}
          url="https://adamrahman126303.typeform.com/to/aYvfMI"
          hideHeaders
          hideFooter
          buttonText="Go!"
          style={{ top: 100 }}
          ref={tf => {
            this.typeformEmbed = tf;
          }}
        />
        <button type="button" class="btn btn-outline-primary" onClick={this.openForm} style={{ cursor: 'pointer' }}>
          SURVEY
        </button>
      </>
    );
  }
}

export default Survey;