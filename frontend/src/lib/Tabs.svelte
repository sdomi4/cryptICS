<!-- from https://svelte.dev/repl/cf05bd4a4ca14fb8ace8b6cdebbb58da?version=4.2.17-->

<script>
    import { createEventDispatcher } from 'svelte';
    export let tabs = [];
    export let activeTabValue = 1;

    const dispatch = createEventDispatcher();

    const handleClick = tabValue => () => {
        activeTabValue = tabValue;
        dispatch('tabChange', { tabValue });
    };
  </script>
  
  <ul>
  {#each tabs as tab}
      <li class={activeTabValue === tab.value ? 'active' : ''}>
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <span on:click={handleClick(tab.value)}>{tab.label}</span>
      </li>
  {/each}
  </ul>
  {#each tabs as tab}
      {#if activeTabValue == tab.value}
      <div class="box">
          <svelte:component this={tab.component} {...tab.props}/>
      </div>
      {/if}
  {/each}
  <style>
      .box {
          margin-bottom: 10px;
          padding: 40px;
          border: 1px solid #dee2e6;
      border-radius: 0 0 .5rem .5rem;
      border-top: 0;
      min-height: 400px;
      }
    ul {
      display: flex;
      flex-wrap: nowrap;
      padding-left: 0;
      margin-bottom: 0;
      list-style: none;
      border-bottom: 1px solid #dee2e6;
    }
      li {
          margin-bottom: -1px;
      }
  
    span {
      border: 1px solid transparent;
      border-top-left-radius: 0.25rem;
      border-top-right-radius: 0.25rem;
      display: block;
      padding: 0.5rem 1rem;
      cursor: pointer;
      text-wrap: nowrap;
    }
  
    span:hover {
      border-color: #e9ecef #e9ecef #dee2e6;
    }
  
    li.active > span {
      color: #495057;
      background-color: #fff;
      border-color: #dee2e6 #dee2e6 #fff;
    }
  </style>