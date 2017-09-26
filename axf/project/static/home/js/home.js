$(document).ready(function(){
    setTimeout(function(){
        swiper1()
//swiper2() swiper1() 是下面的二次轮播，将这个写在 这个里面，
//是为了延迟一秒钟开始轮播，利用这个时间，将图片加载上来
        swiper2()
    },100)
})

function swiper1() {
    var mySwiper1 = new Swiper('#topSwiper', {
        direction: 'horizontal',
        loop: true,
        speed: 500,
        autoplay: 2000,
        pagination: '.swiper-pagination',
        control: true,
    });
};

function swiper2() {
    var mySwiper2 = new Swiper('#swiperMenu', {
        slidesPerView: 3,
        paginationClickable: true,
        spaceBetween: 2,
        loop: false,
    });
};