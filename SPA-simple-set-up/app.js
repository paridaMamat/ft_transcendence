/*const routes = {
    '/': homePage,
    '/about': aboutPage,
    '/create_account': createAccountPage,
    '/login': loginPage,
    '/logout': logoutPage,
    '/profile': profilePage,
    '/404': notFoundPage,

};

const notFoundPage = () => {
    document.body.innerHTML =
    <section>
      <h1>404</h1>
      <p>Page not found</p>
    </section>
  ;
};*/

const app = {
  pages: [],
  show: new Event('show'),
  init: function(){
      app.pages = document.querySelectorAll('.page');
      app.pages.forEach((pg)=>{
          pg.addEventListener('show', app.pageShown);
      })
      
      document.querySelectorAll('.nav-link').forEach((link)=>{
          link.addEventListener('click', app.nav);
      })
      history.replaceState({}, 'Home', '#home');
      window.addEventListener('popstate', app.poppin);
  },
  nav: function(ev){
      ev.preventDefault();
      let currentPage = ev.target.getAttribute('data-target');
      document.querySelector('.active').classList.remove('active');
      document.getElementById(currentPage).classList.add('active');
      console.log(currentPage)
      history.pushState({}, currentPage, `#${currentPage}`);
      document.getElementById(currentPage).dispatchEvent(app.show);
  },
  pageShown: function(ev){
      console.log('Page', ev.target.id, 'just shown');
      let h1 = ev.target.querySelector('h1');
      h1.classList.add('big')
      setTimeout((h)=>{
          h.classList.remove('big');
      }, 1200, h1);
  },
  poppin: function(ev){
      console.log(location.hash, 'popstate event');
      let hash = location.hash.replace('#' ,'');
      document.querySelector('.active').classList.remove('active');
      document.getElementById(hash).classList.add('active');
      console.log(hash)
      //history.pushState({}, currentPage, `#${currentPage}`);
      document.getElementById(hash).dispatchEvent(app.show);
  }
}

document.addEventListener('DOMContentLoaded', app.init);