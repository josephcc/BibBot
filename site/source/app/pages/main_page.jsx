import React from 'react';
import xhttp from 'xhttp/native'

export default class MainPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {citations: []};
  }

  componentDidMount() {
    xhttp({
      url: '/api/list',
      method: 'get'
    }).then( (data) => this.setState({citations: data.data}) );
    this.componentDidUpdate();
  }

  componentDidUpdate(prev, next) {
    $('.bibtex_input').each( function (idx, dom) {
      $('.bibtex_conference_template').remove();
      $('#' + dom.id + '_display').BibtexJS( {
        BibtexString: $('#' + dom.id).text(),
        TemplateString: $("#bibtex-conference-template").text()
      });
    } );
  }

  render() {
    return (
      <div id='main_page'>
      { this.state.citations.map( function(cite) {
        return (
          <div className='citation' key={cite.id}>
            <div className='bibtex' id={'bibtex_' + cite.id + '_display'}></div>
            <div className='domain'>{cite.domain}</div>
            <div className='channel'>{'#' + cite.channel}</div>
            <div className='user'>{'@' + cite.user}</div>
            <div className='time'>{'-' + cite.time}</div>
            <div className='text'>{'> ' + cite.text}</div>
            <a href={cite.url} className='url' target="_blank">link</a>
            <script type='text/template' className='bibtex_input' id={"bibtex_" + cite.id}>
              {cite.bibtex}
            </script>
            <hr/>
          </div>
        );
      } ) }
    <script id="bibtex-conference-template" type="text/template">
        <div className="bibtex_conference_template">
            <div className="if author" style={{fontWeight: 'bold', fontSize: 'medium', paddingTop: '30px'}}>
                <span className="title"></span>
                <span className="if year"> (<span className="conference" style={{color: '#000'}}></span><span className="year" style={{color: '#000'}}></span>)</span>
                <span className="if url" style={{marginLeft: '20px'}}>
                    <a className="url" style={{color: 'black', fontSize: 'small'}}>(view online)</a>
                </span>
            </div>
            <div style={{marginLeft: '10px', marginBottom: '5px'}}>
                <span className="author"></span>. <span className="booktitle"></span>.
            </div>
        </div>
    </script>
      </div>
    );
  }
}
