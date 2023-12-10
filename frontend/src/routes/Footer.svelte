<script>
    import github from '../images/github-mark.png'
</script>

<footer>
    <div class="made">
        Made by Dominik Schenker, supported by Josef Schuler & Ron Porath, SecProj HS23
    </div>
    <div class="footercontainer">
        <a href="https://hslu.ch">Docs</a>
        <div class ="github">
            <a href="https://github.com/sdomi4"><img src={github} alt="GitHub Link" width=25px height=25px></a>
        </div>
        <a href="mailto:dominik.schenker@stud.hslu.ch">Email</a>
    </div>
</footer>

<style>
    .footercontainer {
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: "Roboto", sans-serif;
    }
    .made {
        margin-bottom: 5px;
        font-family: "Roboto", sans-serif;
    }
    footer a {
    margin: 0 10px;
    text-decoration: none;
    color: #333;
    }

    footer a:hover {
        color: #666;
    }

    footer {
        background-color: #f9f9f9;
        padding: 20px;
        text-align: center;
        position: relative;
        bottom: 0;
        width: 100%;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
        }
</style>