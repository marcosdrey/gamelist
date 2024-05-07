$(document).ready(function() {
    $('[data-topic-like]').submit(function(e) {
        e.preventDefault();
        const topic_id = $('[data-topic-btn-like]').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method: "POST",
            url:url,
            headers:{'X-CSRFToken': token},
            data:{
                'topic_id':topic_id
            },
            success:function(response){
                if(response.dislike_was_active===true) {
                    $('[data-topic-icdislike-none]').removeClass('fa-solid')
                    $('[data-topic-icdislike-none]').addClass('fa-regular')
                    $('[data-topic-icdislike-fulfilled]').removeClass('fa-solid')
                    $('[data-topic-icdislike-fulfilled]').addClass('fa-regular')
                    dislike=$('[data-topic-dislikes-count]').text()
                    parseInt(dislike)
                    dislike=dislike-1
                    $('[data-topic-dislikes-count]').text(dislike)
                }
                if(response.liked===true){
                    $('[data-topic-iclike-none]').removeClass('fa-regular')
                    $('[data-topic-iclike-none]').addClass('fa-solid')
                    $('[data-topic-iclike-fulfilled]').removeClass('fa-regular')
                    $('[data-topic-iclike-fulfilled]').addClass('fa-solid')
                } else {
                    $('[data-topic-iclike-none]').removeClass('fa-solid')
                    $('[data-topic-iclike-none]').addClass('fa-regular')
                    $('[data-topic-iclike-fulfilled]').removeClass('fa-solid')
                    $('[data-topic-iclike-fulfilled]').addClass('fa-regular')
                }
                like=$('[data-topic-likes-count]').text(response.likes_count)
                parseInt(like)
            },
            error:function(response){
                console.log("Failed ", response)
            }
        })
    })
    $('[data-topic-dislike]').submit(function(e) {
        e.preventDefault()
        const topic_id = $('[data-topic-btn-dislike]').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')
        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},
            data: {
                'topic_id': topic_id
            },
            success:function(response){
                if (response.like_was_active===true) {
                    $('[data-topic-iclike-none]').removeClass('fa-solid')
                    $('[data-topic-iclike-none]').addClass('fa-regular')
                    $('[data-topic-iclike-fulfilled]').removeClass('fa-solid')
                    $('[data-topic-iclike-fulfilled]').addClass('fa-regular')
                    like=$('[data-topic-likes-count]').text()
                    parseInt(like)
                    like=like-1
                    $('[data-topic-likes-count]').text(like)
                }
                if (response.disliked===true) {
                    $('[data-topic-icdislike-none]').removeClass('fa-regular')
                    $('[data-topic-icdislike-none]').addClass('fa-solid')
                    $('[data-topic-icdislike-fulfilled]').removeClass('fa-regular')
                    $('[data-topic-icdislike-fulfilled]').addClass('fa-solid')
                } else {
                    $('[data-topic-icdislike-none]').removeClass('fa-solid')
                    $('[data-topic-icdislike-none]').addClass('fa-regular')
                    $('[data-topic-icdislike-fulfilled]').removeClass('fa-solid')
                    $('[data-topic-icdislike-fulfilled]').addClass('fa-regular')
                }
                dislike=$('[data-topic-dislikes-count]').text(response.dislikes_count)
                parseInt(dislike)
            },
            error:function(response){
                console.log("Failed ",response)
            }
        })
        
    })
    
    $('[data-comment-like]').submit(function(e) {
        e.preventDefault()
        const comment_id = $(this).find('[data-comment-btn-like]').val()
        const token = $(this).find('input[name=csrfmiddlewaretoken]').val()
        const url = $(this).attr('action')
        const $self = $(this)
        const $container = $self.closest('[data-comment-container-btns]')
        $.ajax({
            method: 'POST',
            url: url,
            headers: {"X-CSRFToken": token},
            data: {
                'comment_id': comment_id,
            },
            success:function(response){
                if(response.dislike_was_active===true) {
                    $container.find('[data-comment-icdislike-none]').removeClass('fa-solid')
                    $container.find('[data-comment-icdislike-none]').addClass('fa-regular')
                    $container.find('[data-comment-icdislike-fulfilled]').removeClass('fa-solid')
                    $container.find('[data-comment-icdislike-fulfilled]').addClass('fa-regular')
                    dislike=$container.find('[data-comment-dislikes-count]').text()
                    parseInt(dislike)
                    dislike=dislike-1
                    $container.find('[data-comment-dislikes-count]').text(dislike)
                }
                if (response.liked===true) {
                    $self.find('[data-comment-iclike-none]').removeClass('fa-regular')
                    $self.find('[data-comment-iclike-none]').addClass('fa-solid')
                    $self.find('[data-comment-iclike-fulfilled]').removeClass('fa-regular')
                    $self.find('[data-comment-iclike-fulfilled]').addClass('fa-solid')
                } else {
                    $self.find('[data-comment-iclike-none]').removeClass('fa-solid')
                    $self.find('[data-comment-iclike-none]').addClass('fa-regular')
                    $self.find('[data-comment-iclike-fulfilled]').removeClass('fa-solid')
                    $self.find('[data-comment-iclike-fulfilled]').addClass('fa-regular')
                }
                like=$self.find('[data-comment-likes-count]').text(response.likes_count)
                parseInt(like)
            },
            error:function(response){
                console.log('Failed ', response)
            }
        }) 
    })
    $('[data-comment-dislike]').submit(function(e) {
        e.preventDefault()
        const comment_id = $(this).find('[data-comment-btn-dislike]').val()
        const token = $(this).find('input[name=csrfmiddlewaretoken]').val()
        const url = $(this).attr('action')
        const $self = $(this)
        const $container = $self.closest('[data-comment-container-btns]')
        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},
            data: {
                'comment_id': comment_id
            },
            success:function(response){
                if(response.like_was_active===true) {
                    $container.find('[data-comment-iclike-none]').removeClass('fa-solid')
                    $container.find('[data-comment-iclike-none]').addClass('fa-regular')
                    $container.find('[data-comment-iclike-fulfilled]').removeClass('fa-solid')
                    $container.find('[data-comment-iclike-fulfilled]').addClass('fa-regular')
                    like=$container.find('[data-comment-likes-count]').text()
                    parseInt(like)
                    like=like-1
                    $container.find('[data-comment-likes-count]').text(like)
                }
                if (response.disliked===true) {
                    $self.find('[data-comment-icdislike-none]').removeClass('fa-regular')
                    $self.find('[data-comment-icdislike-none]').addClass('fa-solid')
                    $self.find('[data-comment-icdislike-fulfilled]').removeClass('fa-regular')
                    $self.find('[data-comment-icdislike-fulfilled]').addClass('fa-solid')
                } else {
                    $self.find('[data-comment-icdislike-none]').removeClass('fa-solid')
                    $self.find('[data-comment-icdislike-none]').addClass('fa-regular')
                    $self.find('[data-comment-icdislike-fulfilled]').removeClass('fa-solid')
                    $self.find('[data-comment-icdislike-fulfilled]').addClass('fa-regular')
                }
                dislike=$self.find('[data-comment-dislikes-count]').text(response.dislikes_count)
                parseInt(dislike)
            },
            error:function(response){
                console.log('Failed ', response)
            }
        })
    })
})
