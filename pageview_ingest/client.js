module.exports = {
  /**
   * initializes the object with an endpoint base name
   * @param endpoint: an endpoint string to base the image request
   */
  init: function (endpoint) {
    this.endpoint = endpoint;
  },

  /**
   * sends the page information to the ingestion endpoint
   */
  sendEvent: function () {
    var location = window.location;
    var hostname = location.hostname
      , pathname = location.pathname
      , search = location.search
      , cacheBuster = (new Date()).getTime();
    var url = this.endpoint +
      '?' + cacheBuster +
      '&hostname=' + hostname +
      '&pathname=' + pathname +
      '&search=' + search;
    var img = new Image();
    img.src = url;
    return img;
  }
};
