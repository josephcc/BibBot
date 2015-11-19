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

  toggleSiblings(target, _event) {
    var obj = $(_event.target);
    obj.siblings(target).toggle();
  }

  render() {
    var urlRE = /<https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:;%_\+.~#?&//=]*)>/g;
    var buttonStyle = {fontSize: '80%', paddingTop: '3px', paddingBottom: '4px', paddingLeft: '6px', paddingRight: '6px', margin: '2px'};
    var codeStyle = {display: 'none', border: '1px solid lightgray', background: '#efefef', padding: '10px', marginTop: '1px'};

    return (
      <div id='main_page' className='pure-g'>
        <div className='pure-u-0 pure-u-sm-0-24 pure-u-md-2-24 pure-u-lg-4-24 pure-u-xl-6-24'></div>
        <div className='pure-u-1 pure-u-sm-24-24 pure-u-md-20-24 pure-u-lg-16-24 pure-u-xl-12-24'>
          { this.state.citations.map( function(cite) {
            return (
              <div className='citation' key={cite.id}>
                <div className='bibtex' id={'bibtex_' + cite.id + '_display'}></div>
                <button className="pure-button pure-button-primary" style={buttonStyle}>{cite.domain}</button>
                <button className="pure-button button-secondary" style={buttonStyle}>{'#' + cite.channel}</button>
                <button className="pure-button button-success" style={buttonStyle} onClick={this.toggleSiblings.bind(this, '.text')}>{'@' + cite.user}</button>
                <a href={cite.url} className="pure-button button-warning" target='_blank' style={buttonStyle}>link</a>
                <button className="pure-button button-warning" style={buttonStyle} onClick={this.toggleSiblings.bind(this, '.raw_bibtex')}>bibtex</button>

                <pre className='text' style={codeStyle}>{cite.text.replace(urlRE, '(link)') + ' - ' + cite.time}</pre>
                <pre className='raw_bibtex' style={codeStyle}>
                  {cite.bibtex}
                </pre>

                <script type='text/template' className='bibtex_input' id={"bibtex_" + cite.id}>
                  {cite.bibtex}
                </script>
                <hr/>
              </div>
            );
          }.bind(this) ) }
        </div>
        <div className='pure-u-0 pure-u-sm-0-24 pure-u-md-2-24 pure-u-lg-4-24 pure-u-xl-6-24'></div>
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
